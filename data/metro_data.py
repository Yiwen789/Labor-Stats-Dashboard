url_metro = {'May 2020': 'https://www.bls.gov/news.release/archives/metro_07012020.htm'}
#functions for scraping and cleaning
def scrape_table_b(table_url):
    #get table
    page = requests.get(table_url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find_all('table', {'id': 'lau_metro_m1'})

    #read scraped data into list
    all_rows = []
    for t in table:
        rows = t.find_all('tr')
        for row in rows:
            value = row.get_text()
            all_rows.append(value)

    #convert list to dataframe
    df = pd.DataFrame(all_rows)
    return df

def split_table(df):
        df = df[0].str.split('\n', expand = True)
        return df
split_df = split_table(scrape_table_b(url_metro['May 2020']))

df_lbf = {}
df_unemp = {}

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
          'Colorado', 'Connecticut', 'Delaware','District of Columbia', 'Florida',
          'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
          'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
          'Maryland', 'Massachusetts', 'Michigan', 'Minnesota','Mississippi',

          'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
          'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
          'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania','Rhode Island',
          'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
          'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin',
          'Wyoming']

split_df = split_table(scrape_table_b(url_metro['May 2020']))
for i in states:
    start_idx = split_df[1].values.tolist().index(i)
    if i != 'Wyoming':
        next = states[states.index(i) + 1]
        end_idx = split_df[1].values.tolist().index(next)
    else:
        end_idx = 443
    data_lbf = split_df[start_idx + 1: end_idx].iloc[:, [3, 5]]
    data_unemp = split_df[start_idx + 1: end_idx].iloc[:, [7, 9]]
    data_lbf.columns = ['Apr 2020', 'May 2020']
    data_unemp.columns = ['Apr 2020', 'May 2020']
    df_lbf[i] = data_lbf
    df_unemp[i] = data_unemp
