# Price Scraper + Currency Converter\n\nA Python project that scrapes book prices from books.toscrape.com, converts GBP to USD (1.36) using an API, saves to CSV/JSON, and plots with matplotlib. Built for Data Analytics coursework, demonstrating web scraping (BeautifulSoup), API handling, regex, and error handling.\n\n## Features\n- Scrapes book titles and prices\n- Converts GBP to USD\n- Saves to CSV/JSON\n- Plots price comparisons\n\n## Setup\n1. Clone repo: \n2. Install dependencies: Collecting pandas==2.2.3 (from -r requirements.txt (line 1))
  Downloading pandas-2.2.3-cp313-cp313-win_amd64.whl.metadata (19 kB)
Collecting requests==2.32.3 (from -r requirements.txt (line 2))
  Downloading requests-2.32.3-py3-none-any.whl.metadata (4.6 kB)
Collecting beautifulsoup4==4.12.3 (from -r requirements.txt (line 3))
  Downloading beautifulsoup4-4.12.3-py3-none-any.whl.metadata (3.8 kB)
Collecting matplotlib==3.9.2 (from -r requirements.txt (line 4))
  Downloading matplotlib-3.9.2-cp313-cp313-win_amd64.whl.metadata (11 kB)
Collecting python-dotenv==1.0.1 (from -r requirements.txt (line 5))
  Downloading python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
Requirement already satisfied: numpy>=1.26.0 in c:\data-analysis-projects\venv\lib\site-packages (from pandas==2.2.3->-r requirements.txt (line 1)) (2.3.3)
Requirement already satisfied: python-dateutil>=2.8.2 in c:\data-analysis-projects\venv\lib\site-packages (from pandas==2.2.3->-r requirements.txt (line 1)) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in c:\data-analysis-projects\venv\lib\site-packages (from pandas==2.2.3->-r requirements.txt (line 1)) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in c:\data-analysis-projects\venv\lib\site-packages (from pandas==2.2.3->-r requirements.txt (line 1)) (2025.2)
Requirement already satisfied: charset-normalizer<4,>=2 in c:\data-analysis-projects\venv\lib\site-packages (from requests==2.32.3->-r requirements.txt (line 2)) (3.4.3)
Requirement already satisfied: idna<4,>=2.5 in c:\data-analysis-projects\venv\lib\site-packages (from requests==2.32.3->-r requirements.txt (line 2)) (3.10)
Requirement already satisfied: urllib3<3,>=1.21.1 in c:\data-analysis-projects\venv\lib\site-packages (from requests==2.32.3->-r requirements.txt (line 2)) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in c:\data-analysis-projects\venv\lib\site-packages (from requests==2.32.3->-r requirements.txt (line 2)) (2025.8.3)
Requirement already satisfied: soupsieve>1.2 in c:\data-analysis-projects\venv\lib\site-packages (from beautifulsoup4==4.12.3->-r requirements.txt (line 3)) (2.8)
Requirement already satisfied: contourpy>=1.0.1 in c:\data-analysis-projects\venv\lib\site-packages (from matplotlib==3.9.2->-r requirements.txt (line 4)) (1.3.3)
Requirement already satisfied: cycler>=0.10 in c:\data-analysis-projects\venv\lib\site-packages (from matplotlib==3.9.2->-r requirements.txt (line 4)) (0.12.1)
Requirement already satisfied: fonttools>=4.22.0 in c:\data-analysis-projects\venv\lib\site-packages (from matplotlib==3.9.2->-r requirements.txt (line 4)) (4.59.2)
Requirement already satisfied: kiwisolver>=1.3.1 in c:\data-analysis-projects\venv\lib\site-packages (from matplotlib==3.9.2->-r requirements.txt (line 4)) (1.4.9)
Requirement already satisfied: packaging>=20.0 in c:\data-analysis-projects\venv\lib\site-packages (from matplotlib==3.9.2->-r requirements.txt (line 4)) (25.0)
Requirement already satisfied: pillow>=8 in c:\data-analysis-projects\venv\lib\site-packages (from matplotlib==3.9.2->-r requirements.txt (line 4)) (11.3.0)
Requirement already satisfied: pyparsing>=2.3.1 in c:\data-analysis-projects\venv\lib\site-packages (from matplotlib==3.9.2->-r requirements.txt (line 4)) (3.2.4)
Requirement already satisfied: six>=1.5 in c:\data-analysis-projects\venv\lib\site-packages (from python-dateutil>=2.8.2->pandas==2.2.3->-r requirements.txt (line 1)) (1.17.0)
Downloading pandas-2.2.3-cp313-cp313-win_amd64.whl (11.5 MB)
   ---------------------------------------- 11.5/11.5 MB 1.0 MB/s  0:00:11
Downloading requests-2.32.3-py3-none-any.whl (64 kB)
Downloading beautifulsoup4-4.12.3-py3-none-any.whl (147 kB)
Downloading matplotlib-3.9.2-cp313-cp313-win_amd64.whl (7.8 MB)
   ---------------------------------------- 7.8/7.8 MB 1.1 MB/s  0:00:07
Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
Installing collected packages: requests, python-dotenv, beautifulsoup4, pandas, matplotlib
  Attempting uninstall: requests
    Found existing installation: requests 2.32.5
    Uninstalling requests-2.32.5:
      Successfully uninstalled requests-2.32.5
  Attempting uninstall: python-dotenv
    Found existing installation: python-dotenv 1.1.1
    Uninstalling python-dotenv-1.1.1:
      Successfully uninstalled python-dotenv-1.1.1
  Attempting uninstall: beautifulsoup4
    Found existing installation: beautifulsoup4 4.13.5
    Uninstalling beautifulsoup4-4.13.5:
      Successfully uninstalled beautifulsoup4-4.13.5
  Attempting uninstall: pandas
    Found existing installation: pandas 2.3.2
    Uninstalling pandas-2.3.2:
      Successfully uninstalled pandas-2.3.2
  Attempting uninstall: matplotlib
    Found existing installation: matplotlib 3.10.6
    Uninstalling matplotlib-3.10.6:\n3. Set  in \n4. Run \n\n## Output\n- : Price data\n- : Price data\n- : Price comparison plot\n\n## Dependencies\nSee  for libraries (requests, beautifulsoup4, matplotlib, pandas, python-dotenv).
# Price-Scraper-CurrencyConversion
