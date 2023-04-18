import asyncio
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def get_llama_models():
    return [
        "7B/ggml-model-q4_0.bin",
        "vicuna/ggml-vicuna-13b-4bit.bin"
    ]

async def llm(
    prompt: str,
    context: int = 512,
    interactive_first: bool = False,
    interactive: bool = False,
    model: str = "7B/ggml-model-q4_0.bin",
    n: int = 10,
    r: str = "### User:",
    repeat_penalty: float = 1.4,
    temp: float = 0.0,
    threads: int = 6,
) -> str:
    llama_path = getenv("LLAMA_PATH")
    cmd = [
        llama_path + "main",
        "--ignore-eos",
        "--repeat_penalty", str(repeat_penalty),
        "--temp", str(temp),
        "-c", str(context),
        "-m", llama_path + "models/" + model,
        "-n", str(n),
        "-p", prompt,
        "-t", str(threads),
    ]

    if interactive:
        cmd.append("-i")
        if interactive_first:
            cmd.append("-interactive-first")

        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        output = ""
        while True:
            line = await proc.stdout.readline()
            if line == b'' and proc.poll() is not None:
              break
            output += line.decode('utf-8')
            print(line.decode('utf-8').strip())

        await proc.wait()
        return output
    else:
      proc = await asyncio.create_subprocess_exec(
          *cmd,
          stdout=asyncio.subprocess.PIPE,
          stderr=asyncio.subprocess.PIPE,
      )

      stdout, stderr = await proc.communicate()

      print(stdout.decode("UTF-8"))
      return stdout.decode("UTF-8")
