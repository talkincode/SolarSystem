import asyncio

async def main():
    from solarsystem.main import AsyncSolarSystem
    await AsyncSolarSystem().start_game()


if __name__ == "__main__":
    asyncio.run(main())