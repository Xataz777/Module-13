import asyncio

async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования')
    for a in range(1, 5):
        await asyncio.sleep(7 - power)
        print (f'Силач {name} поднял шар номер {a}')
    print(f'Силач {name} закончил соревнования')


async def start_tournament():
    strongman1 = asyncio.create_task(start_strongman('Паша', 3))
    strongman2 = asyncio.create_task(start_strongman('Денис', 4))
    strongman3 = asyncio.create_task(start_strongman('Аполлон', 5))
    await strongman1
    await strongman2
    await strongman3


asyncio.run(start_tournament())
