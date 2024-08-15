## Summary
The goal of this project is to determine whether members of Congress achieve higher returns when trading stocks in industries related to the committees they serve on. The underlying hypothesis is that a Congress member would have more intimate knowledge of a particular industry if they serve on a related congressional committee. The final results indicate a statistically significant correlation between the semantic similarity of the committee and the stock industry, and the realized gains.


## Data Collection
The data for this project was pulled from three sources. The congressional trades were taken from [Quiver Quant](https://www.quiverquant.com/congresstrading/) via their API, covering trades from 07-25-2014 to 03-03-2023. The industries were scrapped from [Finviz](https://finviz.com) using Selenium. Stock prices on trade dates and current stock prices were obtained from [Alpaca](https://alpaca.markets) using their API. The stock prices were split-adjusted to prevent errors.


## Calculate Profits
To calculate profits, we must make several assumptions:

* Issue:
The congressional trades are from a fixed date window, from 2014-07-25 to 2023-03-03.
Due to this window, we do not have all trades for each Senator.

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


