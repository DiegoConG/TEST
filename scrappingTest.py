import asyncio
from pyppeteer import launch
from todoist_api_python.api import TodoistAPI

async def extractData(chrome_path, url):

    #Inizializing browser
    browser = await launch(executablePath=chrome_path, headless=True)
    page = await browser.newPage()

    try:
        await page.goto(url)

        await page.waitForSelector('.list-wrapper-with-margins', {'timeout': 10000})

        #Identify table
        tasksTable = await page.querySelector('#board > div:nth-child(6) > div > div.list-cards.u-fancy-scrollbar.js-list-cards.has-margin-bottom')
        if tasksTable is None:
            print("Task table not found.")
            return
        else:
             #FormatData
            cards = await tasksTable.querySelectorAllEval('.list-card-title', r'(elements) => elements.map(el => el.textContent.replace(/^N\.º \d+/, "").trim())')

            uploadData(cards)

    finally:
        await browser.close()
        

def uploadData(tasks):
    for task in tasks[:5]:
        try:
            task = api.add_task(
                content=task,
                due_string="tomorrow at 16:00",
                due_lang="en",
                priority=4,
            )
            print("Task Added Successfully")
        except Exception as error:
            print("Error adding the task: " + error)
            

if __name__ == '__main__':
    
    #Global variables
    api = TodoistAPI("API to be added") #Personal API
    chromium_path = r'Path to be added' #Chromium Version used: 117.0.5913.0
    url = 'https://trello.com/b/QvHVksDa/personal-work-goals' #Trello Taskboard link

    asyncio.get_event_loop().run_until_complete(extractData(chromium_path, url))
