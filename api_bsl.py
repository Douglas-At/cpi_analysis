import os 
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import requests
import pandas as pd
load_dotenv()

class APIbureau:
    """
    A class to interact with the BLS API and handle data requests for various Consumer Price Index (CPI) metrics.
    """

    def __generic_request(self,series_id,start_year,end_year):
        """
        Generic method to request data from the BLS API.

        Args:
            series_id (str): The identifier for the data series.
            start_year (int): Starting year for the request.
            end_year (int): Ending year for the request.

        Returns:
            tuple:
                pd.DataFrame: The data retrieved from the API in DataFrame format.
                int: The HTTP status code of the response.
        """

        url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
        api_key = os.getenv("API_KEY")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {api_key}"
        }
        payload = {
            "seriesid": [series_id],
            "startyear": str(start_year),  
            "endyear": str(end_year)     
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "REQUEST_SUCCEEDED":
                return pd.DataFrame.from_records(data["Results"]["series"][0]["data"]),response.status_code
            else:
                print("Request failed: ", data["message"])
                return pd.DataFrame(),response.status_code
        else:
            print("HTTP error: ",response.status_code)
            return pd.DataFrame(),response.status_code
        
    def __single_series(self,start_year,end_year,ticker):
        """
        Handles large date ranges by dividing the request into smaller chunks if necessary.

        Args:
            start_year (int): Starting year for the data.
            end_year (int): Ending year for the data.
            ticker (str): The series identifier.

        Returns:
            tuple:
                pd.DataFrame: Concatenated DataFrame with the requested data.
                int: The HTTP status code of the last response.
        """
        list_df = []
        if end_year - start_year >10:
            for _ in range(int((end_year - start_year)/10)+1):
                df, status = self.__generic_request(start_year=start_year,end_year=end_year,series_id=ticker)
                if df.empty and status == 200:
                    raise ValueError("Empty Datarfame, not by bad Request")
                start_year += 10 
                
                list_df.append(df)

            df = pd.concat(list_df, ignore_index=True)
        else:
            df, status = self.__generic_request(start_year=start_year,end_year=end_year,series_id=ticker)
        return df,status
            
    def __save_dataframe(self, df,file_extension,name):
        """
        Saves the provided DataFrame to a file in the specified format.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            file_extension (str): The file format ('xlsx', 'csv', 'txt').
            name (str): The base name of the file.
        """

        if file_extension == 'xlsx':
            df.to_excel(f"{name}.xlsx", index=False)
        elif file_extension == 'csv':
            df.to_csv(f"{name}.csv", index=False)
        elif file_extension == 'txt':
            df.to_csv(f"{name}.txt", sep=';', index=False)
        else:
            print(f"Unsupported format '{file_extension}'. Defaulting to 'xlsx'.")
            df.to_excel(f"{name}.xlsx", index=False)
    
    def __clean_dataframe(self, df):
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['period'].str[1:], errors='coerce',format='%Y-%m')
        df = df.sort_values(by='date')
        df['value'] = df['value'].astype(float)
        return df
    
    def process_cpi_series(self, start_year: int, end_year: int, ticker: str, output_filename: str, plot_title: str, format: str = "xlsx", plot: bool = False):
        """
        General method to process CPI series data.
        
        Args:
            start_year (int): Start year for the CPI data.
            end_year (int): End year for the CPI data.
            ticker (str): Ticker for the CPI series.
            output_filename (str): Name of the output file.
            plot_title (str): Title for the plot.
            format (str): File format for saving the data (default: 'xlsx').
            plot (bool): Whether to plot the data (default: False).
        """
        df, status = self.__single_series(start_year=start_year, end_year=end_year, ticker=ticker)
        if df.empty and status == 200:
            raise ValueError("Empty Datarfame, not by bad Request")
        df = self.__clean_dataframe(df)
        self.__save_dataframe(df, format, output_filename)
        if plot:
            PlotSeries().plot_series_cpi(df, start_year, end_year, plot_title).show()

    def cpi_all_items(self, start_year: int, end_year: int, format: str = "xlsx", plot: bool = False):
        self.process_cpi_series(start_year, end_year, "CUSR0000SA0", f"CPI_ALL_ITEMS_{start_year}_{end_year}", "CPI_ALL_ITEMS", format, plot)

    def cpi_all_items_less_food_energy(self, start_year: int, end_year: int, format: str = "xlsx", plot: bool = False):
        self.process_cpi_series(start_year, end_year, "CUSR0000SA0L1E", f"CPI_ALL_ITEMS_LESS_FOOD_ENERGY_{start_year}_{end_year}", "CPI_ALL_ITEMS_LESS_FOOD_ENERGY", format, plot)

    def cpi_food(self, start_year: int, end_year: int, format: str = "xlsx", plot: bool = False):
        self.process_cpi_series(start_year, end_year, "CUSR0000SAF1", f"CPI_FOOD_{start_year}_{end_year}", "CPI_FOOD", format, plot)

    def cpi_energy(self, start_year: int, end_year: int, format: str = "xlsx", plot: bool = False):
        self.process_cpi_series(start_year, end_year, "CUSR0000SA0E", f"CPI_ENERGY_{start_year}_{end_year}", "CPI_ENERGY", format, plot)

    def cpi_apparel(self, start_year: int, end_year: int, format: str = "xlsx", plot: bool = False):
        self.process_cpi_series(start_year, end_year, "CUSR0000SAA", f"CPI_APPAREL_{start_year}_{end_year}", "CPI_APPAREL", format, plot)

    def cpi_education_communication(self, start_year: int, end_year: int, format: str = "xlsx", plot: bool = False):
        self.process_cpi_series(start_year, end_year, "CUSR0000SAE", f"CPI_EDUCATION_COMMUNICATION_{start_year}_{end_year}", "CPI_EDUCATION_COMMUNICATION", format, plot)

    def cpi_other_goods_services(self, start_year: int, end_year: int, format: str = "xlsx", plot: bool = False):
        self.process_cpi_series(start_year, end_year, "CUSR0000SAG", f"CPI_OTHER_GOODS_SERVICES_{start_year}_{end_year}", "CPI_OTHER_GOODS_SERVICES", format, plot)

    def cpi_medical_care(self, start_year: int, end_year: int, format: str = "xlsx", plot: bool = False):
        self.process_cpi_series(start_year, end_year, "CUSR0000SAM", f"CPI_MEDICAL_CARE_{start_year}_{end_year}", "CPI_MEDICAL_CARE", format, plot)

    def cpi_recreation(self, start_year: int, end_year: int, format: str = "xlsx", plot: bool = False):
        self.process_cpi_series(start_year, end_year, "CUSR0000SAR", f"CPI_RECREATION_{start_year}_{end_year}", "CPI_RECREATION", format, plot)

    def cpi_transportation(self, start_year: int, end_year: int, format: str = "xlsx", plot: bool = False):
        self.process_cpi_series(start_year, end_year, "CUSR0000SAT", f"CPI_TRANSPORTATION_{start_year}_{end_year}", "CPI_TRANSPORTATION", format, plot)


            
        

class PlotSeries:

    def plot_series_cpi(self, df,start_year,end_year, name):
        """
        Plots the CPI series
        """
        plt.figure(figsize=(10, 5))
        plt.plot(df['date'], df['value'], color='brown', linewidth=1.5)
        plt.title(f'{name.replace("_"," ")} | {start_year} - {end_year}')
        plt.xlabel('Month')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt

    
    
    
if __name__ == "__main__":
    api = APIbureau()
    api.cpi_medical_care(start_year=2000,end_year=2023,format="txt", plot=True)
    # df = pd.read_excel("base(1).xlsx")
    # print(df.dtypes)
