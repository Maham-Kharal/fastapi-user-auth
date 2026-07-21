import asyncio
import os
import sys

# Ensure project paths are in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, "..", "..")))

from app.services.retrieval_eval import run_eval_harness_logic


async def main():
    print("=== Starting shared RAG Evaluation Harness ===")
    try:
        result = await run_eval_harness_logic(write_report_file=True)
        print("\nEvaluation Summary:")
        for cfg in result["configs"]:
            print(
                f"- {cfg['name']}: Hit Rate = {cfg['hit_rate']*100:.1f}% "
                f"({cfg['hits']}/{cfg['total']}) | Chunks = {cfg['num_chunks']}"
            )
        print("\nWritten detailed report to artifacts.")
    except Exception as e:
        print(f"Error running evaluation: {e}")


if __name__ == "__main__":
    asyncio.run(main())
