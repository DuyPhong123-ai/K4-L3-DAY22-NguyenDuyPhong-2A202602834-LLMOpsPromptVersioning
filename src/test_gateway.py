"""Kiểm tra chat và embeddings của gateway trước khi chạy RAG/RAGAS."""
import argparse
import re

import config
from openai import OpenAI


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=config.OPENAI_MODEL)
    parser.add_argument("--skip-embeddings", action="store_true")
    args = parser.parse_args()

    if not config.OPENAI_API_KEY:
        raise SystemExit("Thiếu OPENAI_API_KEY trong .env.")

    with OpenAI(
        api_key=config.OPENAI_API_KEY,
        base_url=config.OPENAI_BASE_URL or None,
        timeout=30,
        max_retries=0,
    ) as client:
        try:
            response = client.chat.completions.create(
                model=args.model,
                messages=[{"role": "user", "content": "Reply with exactly: PONG"}],
                max_tokens=256,
            )
            content = response.choices[0].message.content
            print("model:", args.model)
            print("response:", content)
            if not content or content.strip() != "PONG":
                raise SystemExit("Chat chưa trả về PONG như yêu cầu.")

            if not args.skip_embeddings:
                response = client.embeddings.create(
                    model=config.OPENAI_EMBEDDING_MODEL,
                    input=["Gateway embedding smoke test."],
                    encoding_format="float",
                )
                if not response.data or not response.data[0].embedding:
                    raise SystemExit("Embeddings trả về vector rỗng.")
                print("embedding model:", config.OPENAI_EMBEDDING_MODEL)
                print("embedding dimensions:", len(response.data[0].embedding))
        except Exception as exc:
            message = str(exc).replace(config.OPENAI_API_KEY, "[REDACTED]")
            message = re.sub(r"sk-[A-Za-z0-9_-]{10,}", "[REDACTED]", message)
            raise SystemExit(f"{type(exc).__name__}: {message}") from None


if __name__ == "__main__":
    main()
