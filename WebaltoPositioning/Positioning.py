from Positioning_Monitor import pd, requests, BeautifulSoup, timeit, dt, datetime, ThreadPoolExecutor, warnings

class Position:
    def __init__(self, ticker, updatetype = "All", date = dt.today(), days = 5, file_path = "P:\\Product Specialists\\Tools\\Position Monitor\\"):
        self.days = days
        self.ticker = ticker
        self.updatetype = updatetype
        self.file_path = file_path
        self.__dates = [date - datetime.timedelta(days=i) for i in range(days)]
        self.__tickers = [ticker for i in range(days)]
        self.__starttime = timeit.default_timer()
        warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
        

        
        if self.updatetype == "Rates":
            self.__read_path = self.file_path + self.ticker + "_RatesMD.csv"
            url = "http://webalto/reporting/nodecorate/transfo.action?report=PFI_LDN_ATTRIBUTION_PERFORMANCE&date={}&scenario=portfolioAnalysis&occurrence={}&view=Rates+-+Main+&format=html&expand=-2"
            self.urls = [url for i in range(days)]
            with ThreadPoolExecutor(max_workers=days) as executor:
            ##### All output are put into list name 'results' #####
                self.results = list(executor.map(self.__GetRates, self.urls, self.__tickers, self.__dates))
                
            self.rates = self.__GetPosition(self.__read_path, self.results)
            
        elif self.updatetype == "Fx":
            self.__read_path = self.file_path + self.ticker + "_FX.csv"
            url = "http://webalto/reporting/nodecorate/transfo.action?report=PFI_LDN_ATTRIBUTION_PERFORMANCE&date={}&scenario=portfolioAnalysis&occurrence={}&view=Currencies&format=html&expand=-2"
            self.urls = [url for i in range(days)]
            with ThreadPoolExecutor(max_workers=days) as executor:
            ##### All output are put into list name 'results' #####
                self.results = list(executor.map(self.__GetCCY, self.urls, self.__tickers, self.__dates))
            
            self.fx = self.__GetPosition(self.__read_path, self.results)
            
        elif self.updatetype == "Credit":
            self.__read_path = self.file_path + self.ticker + "_Credit.csv"
            url = "http://webalto/reporting/nodecorate/transfo.action?report=PFI_LDN_ATTRIBUTION_PERFORMANCE&date={}&scenario=portfolioAnalysis&occurrence={}&view=Credit+-+Sectors+-+Currency&format=html&expand=-2"
            self.urls = [url for i in range(days)]
            with ThreadPoolExecutor(max_workers=days) as executor:
            ##### All output are put into list name 'results' #####
                self.results = list(executor.map(self.__GetCredit, self.urls, self.__tickers, self.__dates))
                
            self.credit = self.__GetPosition(self.__read_path, self.results)
            
        elif self.updatetype == "All":
            self.__read_path = self.file_path + self.ticker + "_RatesMD.csv"
            url = "http://webalto/reporting/nodecorate/transfo.action?report=PFI_LDN_ATTRIBUTION_PERFORMANCE&date={}&scenario=portfolioAnalysis&occurrence={}&view=Rates+-+Main+&format=html&expand=-2"
            self.urls = [url for i in range(days)]
            with ThreadPoolExecutor(max_workers=days) as executor:
                self.results = list(executor.map(self.__GetRates, self.urls, self.__tickers, self.__dates))
                
            self.rates = self.__GetPosition(self.__read_path, self.results)

            self.__read_path = self.file_path + self.ticker + "_FX.csv"
            url = "http://webalto/reporting/nodecorate/transfo.action?report=PFI_LDN_ATTRIBUTION_PERFORMANCE&date={}&scenario=portfolioAnalysis&occurrence={}&view=Currencies&format=html&expand=-2"
            self.urls = [url for i in range(days)]
            with ThreadPoolExecutor(max_workers=days) as executor:
                self.results = list(executor.map(self.__GetCCY, self.urls, self.__tickers, self.__dates))
            
            self.fx = self.__GetPosition(self.__read_path, self.results)              

            self.__read_path = self.file_path + self.ticker + "_Credit.csv"
            url = "http://webalto/reporting/nodecorate/transfo.action?report=PFI_LDN_ATTRIBUTION_PERFORMANCE&date={}&scenario=portfolioAnalysis&occurrence={}&view=Credit+-+Sectors+-+Currency&format=html&expand=-2"
            self.urls = [url for i in range(days)]
            with ThreadPoolExecutor(max_workers=days) as executor:
                self.results = list(executor.map(self.__GetCredit, self.urls, self.__tickers, self.__dates))
                
            self.credit = self.__GetPosition(self.__read_path, self.results)
            
            print("      " + self.ticker + " Process Time: " + str(timeit.default_timer() - self.__starttime))
        else:
            print("UPDATE TYPE DOES NOT EXIST!")
            print("      " + self.ticker + " Process Time: " + str(timeit.default_timer() - self.__starttime))
    
        
    def __GetPosition(self, read_path, results):
        try:
            df_old = pd.read_csv(read_path)
        except:
            df_old = pd.DataFrame()
        df = pd.DataFrame()

        for result in results:            
            df=pd.concat([df, result])          

        df = pd.concat([df_old, df], ignore_index = True) 
        df = df.drop_duplicates(subset=['Date'], keep='last')
        df = df.sort_values(by=['Date'], ascending=False).fillna(0)

        return df        
        
        
    def SavePosition(self, positiontype):       
        try:
            if positiontype == "Rates":
                self.__save_path = self.file_path + self.ticker + "_RatesMD.csv"
                self.rates.to_csv(self.__save_path, index=False)
            elif positiontype == "Fx":
                self.__save_path = self.file_path + self.ticker + "_FX.csv"
                self.fx.to_csv(self.__save_path, index=False)
            elif positiontype == "Credit":
                self.__save_path = self.file_path + self.ticker + "_Credit.csv"
                self.credit.to_csv(self.__save_path, index=False)
            elif positiontype == "All":
                self.__save_path = self.file_path + self.ticker + "_RatesMD.csv"
                self.rates.to_csv(self.__save_path, index=False)
                self.__save_path = self.file_path + self.ticker + "_FX.csv"
                self.fx.to_csv(self.__save_path, index=False)
                self.__save_path = self.file_path + self.ticker + "_Credit.csv"
                self.credit.to_csv(self.__save_path, index=False)
            else:
                print("Position type doesn't exist!")
        except AttributeError:
            print("This position is not updated or it doesn't exists")
       
    def __GetRatesColumns(self, rates, ticker, date):
        # Get Rates Table Headers
        url = rates.format(str(date).replace('-',''), ticker)
        response = requests.get(url).text
        soup = BeautifulSoup(response, features="lxml")

        # find columns
        td_tags = soup.find("table").find("tr", class_ = "view_table_headers").find_all("td")
        columns = []
        for td_tag in td_tags:
            if td_tag.string:
                columns.append(td_tag.string+"  MD(P-B)")
        return columns
    
    
    def __GetRates(self, rates, ticker, date):
    # Get Rates Exposure
    
        url = rates.format(str(date).replace('-',''), ticker)

        try:
            df = pd.DataFrame()

            response = requests.get(url).text
            soup = BeautifulSoup(response, features="lxml")

            tr_tag = soup.find("tr", class_ = "l0") 
            td_tags = tr_tag.find_all("td")
            expo = []
            for td_tag in td_tags:
                if td_tag.get('x:num'):
                    expo.append(float(td_tag.get('x:num')))
                elif td_tag.string:
                    expo.append(" "+td_tag.string)
                else:
                    expo.append(0)
            df[len(df.columns)+1]=(expo)   

            tr_tags = soup.find("table").find_all("tr", class_ = "l1")      
            for tr_tag in tr_tags:
                td_tags = tr_tag.find_all("td")
                expo = []
                for td_tag in td_tags:
                    if td_tag.get('x:num'):
                        expo.append(float(td_tag.get('x:num')))
                    elif td_tag.string:
                        expo.append(td_tag.string)
                    else:
                        expo.append(0)
                df[len(df.columns)+1]=(expo)
            df = df.T

            columns = self.__GetRatesColumns(rates, ticker, date)
            column_name = ["Date"]
            for i in range(0,len(df)):
                for j in range(0,len(columns)):
                    column_name.append(columns[j] + '_' + df.iat[i,0].replace("\xa0 ",""))

            df.drop(df.columns[0], axis = 1, inplace=True)
            df_list = df.stack().tolist()
            df_list.insert(0, str(date))

            df = pd.DataFrame(pd.DataFrame(df_list)).T
            df.columns = column_name

            return df  

        except:
            return
        
        
    def __GetCreditColumns(self, credit, ticker, date):
        # Get Credit Table Headers

        url = credit.format(str(date).replace('-',''), ticker)

        response = requests.get(url).text

        soup = BeautifulSoup(response, features="lxml")

        # find columns
        td_tags = soup.find("table").find("tr", class_ = "view_table_headers").find_all("td")
        DTS=["PTF", "P-B"]
        columns = []
        for td_tag in td_tags:
            if td_tag.string:
                columns.append(td_tag.string)
        return columns

    
    def __GetCredit(self, credit, ticker, date):
        # Get Credit Exposure

        url = credit.format(str(date).replace('-',''), ticker)

        try:        
            df = pd.DataFrame()
            sector = []
            response = requests.get(url).text
            soup = BeautifulSoup(response, features="lxml")
            tr_tags = soup.find("table").find_all("tr")    
            for tr_tag in tr_tags:
                if tr_tag.get("class") == ['l0']:
                    td_tags = tr_tag.find_all("td")
                    expo = []
                    for td_tag in td_tags:

                        if td_tag.get('x:num'):
                            expo.append(float(td_tag.get('x:num')))
                        elif td_tag.string:
                            expo.append(" " + td_tag.string.replace("\xa0 ",""))
                        else:
                            expo.append(0)
                    df[len(df.columns)+1]=expo

                elif tr_tag.get("class") == ['l1']:
                    td_tag = tr_tag.find("td", class_ = "r")
                    sector = td_tag.string.replace("\xa0 ","")

                    td_tags = tr_tag.find_all("td")
                    expo = []
                    for td_tag in td_tags:
                        if td_tag.get('x:num'):
                            expo.append(float(td_tag.get('x:num')))
                        elif td_tag.string:
                            expo.append(td_tag.string.replace("\xa0 ",""))
                        else:
                            expo.append(0)
                    df[len(df.columns)+1]=expo

                elif tr_tag.get("class") == ['l2']:
                    td_tags = tr_tag.find_all("td")

                    expo = []
                    for td_tag in td_tags:
                        if td_tag.get('x:num'):
                            expo.append(float(td_tag.get('x:num')))
                        elif td_tag.string:
                            expo.append(sector + td_tag.string.replace("\xa0 ",""))
                        else:
                            expo.append(0)
                    df[len(df.columns)+1]=expo
                    #pd.concat([df, expo], axis = 1)

            df = df.T


            columns = self.__GetCreditColumns(credit, ticker, date)
            column_name = ["Date"]
            for i in range(0,len(df)):
                for j in range(0,len(columns)):
                    column_name.append(columns[j] + '_' + df.iat[i,0].replace(" \xa0 ",""))

            df.drop(df.columns[0], axis = 1, inplace=True)
            df_list = df.stack().tolist()
            df_list.insert(0, str(date))

            df = pd.DataFrame(pd.DataFrame(df_list)).T
            df.columns = column_name

            return df  

        except:
            return
    

    def __GetCCYColumns(self, ccy, ticker, date):
        # Get Currency Table Headers

        url = ccy.format(str(date).replace('-',''), ticker)

        response = requests.get(url).text

        soup = BeautifulSoup(response, features="lxml")

        # find columns
        wght=["PTF", "P-B"]
        td_tags = soup.find("table").find("tr", class_ = "view_table_headers").find_all("td")
        columns = []
        for td_tag in td_tags:
            if td_tag.string:
                columns.append(td_tag.string+"  "+wght[0])
                columns.append(td_tag.string+"  "+wght[1])

        return columns

    
    def __GetCCY(self, ccy, ticker, date):
        # Get Currency Exposure

        url = ccy.format(str(date).replace('-',''), ticker)

        try:
            df = pd.DataFrame()

            response = requests.get(url).text
            soup = BeautifulSoup(response, features="lxml")
            tr_tags = soup.find("table").find_all("tr", class_ = "l0")      
            for tr_tag in tr_tags:
                td_tags = tr_tag.find_all("td")
                expo = []
                for td_tag in td_tags:
                    if td_tag.get('x:num'):
                        expo.append(float(td_tag.get('x:num')))
                    elif td_tag.string:
                        expo.append(td_tag.string)
                    else:
                        expo.append(0)
                df[len(df.columns)+1]=(expo)
            df = df.T

            columns = self.__GetCCYColumns(ccy, ticker, date)
            column_name = ["Date"]
            for i in range(0,len(df)):
                for j in range(0,len(columns)):
                    column_name.append(columns[j] + '_' + df.iat[i,0].replace("\xa0 ",""))

            df.drop(df.columns[0], axis = 1, inplace=True)
            df_list = df.stack().tolist()
            df_list.insert(0, str(date))

            df = pd.DataFrame(pd.DataFrame(df_list)).T
            df.columns = column_name

            return df  

        except:
            return
