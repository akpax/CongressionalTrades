## Summary
The goal of this project is to determine whether members of Congress achieve higher returns when trading stocks in industries related to the committees they serve on. The underlying hypothesis is that a Congress member would have more intimate knowledge of a particular industry if they serve on a related congressional committee. The final results indicate a statistically significant correlation between the semantic similarity of the committee and the stock industry, and the realized gains.


## Data Collection
The data for this project was pulled from three sources. The congressional trades were taken from [Quiver Quant](https://www.quiverquant.com/congresstrading/) via their API, covering trades from 07-25-2014 to 03-03-2023. The industries were scrapped from [Finviz](https://finviz.com) using Selenium. Stock prices on trade dates and current stock prices were obtained from [Alpaca](https://alpaca.markets) using their API. The stock prices were split-adjusted to prevent errors.

Fuzzy matching with human oversight was used to match Congress member names from Quiver Quant trades to the committee names provided. Common issues included inconsistencies such as missing middle names or initials and the use of commas. Additionally, the bracketed ranges provided by Quiver Quant were not in a standardized format and were standardized using regex.

## Initial Data Exploration
### Quantity of Trades Placed
An analysis of the quantity of trades placed by Congress members between 2014-2023 shows that David Perdue placed the most trades, followed by Josh Gottheimer.
![image](https://github.com/user-attachments/assets/2224b3b9-caf6-4f01-b70c-799b229af436)


### Stock Act Violations
According to the STOCK Act, each Congress member has 45 days to report their trades to prevent trading based on private information derived from their official positions. Unfortunately, there were numerous violations; 119 of the 212 Congress members who traded stocks from 2013-2024 violated the STOCK Act. Top violators, including prolific traders David Perdue and Josh Gottheimer, recorded violations in the hundreds.
![image](https://github.com/user-attachments/assets/c4e642bb-6686-472e-8462-b290ecb0e0e4)
<img width="573" alt="image" src="https://github.com/user-attachments/assets/a13051b2-e1bc-46b0-98f2-a7d5124c7b55">


### Trade Sizes
The majority of trades were in the $15,000 to $50,000 range, with 42 large trades falling within the $1,000,000 to $5,000,000 range.
![image](https://github.com/user-attachments/assets/b1f5a493-e230-48a8-b09c-879862290045)
<img width="291" alt="image" src="https://github.com/user-attachments/assets/ef234072-5685-48aa-9d6b-fd726c46d5ee">


### Traders Who Frequently Made Large Trades:
This section highlights traders who frequently made large trades in the $1,000,000 to $5,000,000 range.
![image](https://github.com/user-attachments/assets/f11205ba-ee9d-4707-be2c-ad06d5491c49)


## Calculate Profits
To calculate profits, we must make several assumptions:

* Issue:
    - The congressional trades are from a fixed date window, from 2014-07-25 to 2023-03-03.  Due to this window, we do not have all trades for each Senator.


* Assumptions:
    - Assume that Congress members are not short selling. This accounts for the edge case where the Congress member bought shares before our window and sold them within the window.

* Implementation:
    - If the shares sold in a transaction bring the total shares to a negative number, the shares_owned will be set to 0, not negative.
    - Profit for the trade will be calculated using the current cost basis.
    - Quiver Quant provides a bracketed range for each trade size. We used the lower bound of the range to calculate the gains.


## Analysis
Google's Universal Sentence Encoder was used to convert the stock industries and committees into vectors. These vectors allow the computer to understand and compare the textual data. The vectors map the words into a latent space, where the proximity of the vectors indicates their similarity. To measure this proximity, the cosine similarity was calculated between the stock industry and committees. Since some Congress members serve on multiple committees, the committee with the highest similarity to the stock was used for the similarity score. This assumes the congress member’s most relevant information will come from the one with the highest similarity score. 


## Results
The realized gains and semantic similarity score are positively correlated, as indicated by a p-value of < 0.005. Although the correlation is small (0.08 for total realized gains and 0.04 for realized gains per year), it still represents a significant edge in the world of stock trading. Interestingly, unrealized gains and unrealized gains per year are negatively correlated with semantic similarity. However, their p-values are above 0.005 and are not statistically significant.

![image](https://github.com/user-attachments/assets/be2ba7a6-4395-4d1f-9033-55025ec1da0c)


