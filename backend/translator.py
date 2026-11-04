import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_NAME = "Helsinki-NLP/opus-mt-en-dra"
HUGGING_FACE_URL = (
    f"https://router.huggingface.co/hf-inference/models/{MODEL_NAME}"
)
MYMEMORY_URL = "https://api.mymemory.translated.net/get"

load_dotenv(PROJECT_ROOT / ".env")


class TamilTranslator:

    def __init__(self):
        self.api_token = os.environ.get("HF_TOKEN")

    @staticmethod
    def _translate_with_mymemory(text):
        query = urlencode({"q": text, "langpair": "en|ta"})
        request = Request(
            f"{MYMEMORY_URL}?{query}",
            headers={"User-Agent": "SLM_TRANSLATOR/1.0"},
        )

        try:
            with urlopen(request, timeout=30) as response:
                result = json.load(response)
        except HTTPError as error:
            raise RuntimeError(
                f"MyMemory returned HTTP {error.code}."
            ) from error
        except URLError as error:
            raise RuntimeError(
                f"Could not connect to MyMemory: {error.reason}"
            ) from error
        except json.JSONDecodeError as error:
            raise RuntimeError("MyMemory returned invalid JSON.") from error

        if not isinstance(result, dict):
            raise RuntimeError("MyMemory returned an unexpected response.")
        if str(result.get("responseStatus")) != "200":
            raise RuntimeError(
                "MyMemory translation failed: "
                f"{result.get('responseDetails', 'unknown error')}"
            )

        response_data = result.get("responseData")
        if not isinstance(response_data, dict):
            raise RuntimeError("MyMemory returned an unexpected response.")

        translation = response_data.get("translatedText")
        if not isinstance(translation, str) or not translation.strip():
            raise RuntimeError("MyMemory returned an empty translation.")
        return translation.strip()

    def translate(self, text):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Input text must be a non-empty string.")

        text = text.strip()
        load_dotenv(PROJECT_ROOT / ".env", override=False)
        self.api_token = os.environ.get("HF_TOKEN")

        if not self.api_token or not self.api_token.strip():
            return self._translate_with_mymemory(text)

        request = Request(
            HUGGING_FACE_URL,
            data=json.dumps({"inputs": f">>tam<< {text}"}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_token.strip()}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=60) as response:
                result = json.load(response)
        except HTTPError as error:
            if error.code == 402:
                return self._translate_with_mymemory(text)
            try:
                details = json.loads(error.read().decode("utf-8"))
                message = details.get("error", details)
            except (UnicodeDecodeError, json.JSONDecodeError):
                message = error.reason
            raise RuntimeError(
                f"Hugging Face translation API returned HTTP "
                f"{error.code}: {message}"
            ) from error
        except URLError as error:
            raise RuntimeError(
                f"Could not connect to Hugging Face: {error.reason}"
            ) from error
        except json.JSONDecodeError as error:
            raise RuntimeError(
                "Hugging Face returned invalid JSON."
            ) from error

        try:
            if isinstance(result, list):
                translation = result[0]["translation_text"]
            else:
                translation = result["translation_text"]
        except (KeyError, IndexError, TypeError) as error:
            raise RuntimeError(
                "Hugging Face returned an unexpected translation response."
            ) from error

        if not isinstance(translation, str) or not translation.strip():
            raise RuntimeError(
                "Hugging Face returned an empty translation."
            )
        return translation.strip()
