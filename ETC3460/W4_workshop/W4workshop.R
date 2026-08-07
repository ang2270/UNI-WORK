
library(quantmod)
options("getSymbols.warning4.0"=FALSE)
getSymbols(Symbols = c("MSFT", "AAPL" ), from="2020-12-01", to="2025-12-31",
           auto.assign=TRUE, warnings=FALSE)

# convert to monthly
msft_M_P = to.monthly(MSFT$MSFT.Adjusted, OHLC=FALSE) 
aapl_M_P = to.monthly(AAPL$AAPL.Adjusted, OHLC=FALSE) 

# merge 2 series monthly 
month_P = merge(msft_M_P,aapl_M_P)
colnames(month_P) <- c("msft","aapl")
head(month_P)
tail(month_P)


#--------------------------------------------
# export to excel

# m_prices.xts = month_P
# m.prices.df <- data.frame(
#   Date = format(as.Date(index(m_prices.xts)), "%Y-%m"),
#   coredata(m_prices.xts),
#   row.names = NULL
# )
# head(m.prices.df)
# 
# writexl::write_xlsx(m.prices.df, "Monthly_prices.xlsx")

#---------------------------------------------



# 1. log return
lr = na.omit(diff(log(month_P)))
colnames(lr) <- c("msft","aapl")
head(lr)  
tail(lr)


# 2. compute sample mean, standard deviation, sharpe ratio
# Assume rf = 3% p.a.

# sample mean for each column, note that 2 = apply over columns
muhat = apply(lr,2,mean)
muhat
# sample variance and standard deviation for each column
sigma2hat = apply(lr,2,var)
sigmahat = apply(lr,2,sd)
# sigmahat = sqrt(sigma2hat)
sigma2hat
sigmahat


# Sharpe ratio
SR = (muhat-0.03/12)/sigmahat
SR


# 3. Compute covariance, correlation
cov.mat = cov(lr)  # covariance
cov.mat
options(digits=5, width=70)
cor.mat = cor(lr) # correlation 
cor.mat 



# 4. Compute GMV weight
w.gmv.1 = (cov.mat[2,2] - cov.mat[1,2]) / (cov.mat[1,1] + cov.mat[2,2] - 2*cov.mat[1,2] )
w.gmv.1


# 5. Compute GMV weight via regression
# The coefficient estimate of β_1 is equal to  0.60161. 
# This is equal to the GMV weights computed for MSFT. 
# Then 1-β_1 is the GMV weight assigned to Apple.
y = lr$aapl 
x = lr$aapl - lr$msft

fit <- lm(y~x)
summary(fit)

w.gmv.2 = fit$coefficients[2]
w.gmv.2



# 6. Compute GMV via covariance matrix

N <- ncol(cov.mat) # N is the number of columns

# GMV weights: w = Sigma^{-1} 1 / (1' Sigma^{-1} 1)
one.vec <- rep(1, N)
sigma.inv.mat <- solve(cov.mat)

w.gmv.3 <- as.vector(sigma.inv.mat %*% one.vec) /
  as.numeric(t(one.vec) %*% sigma.inv.mat %*% one.vec)

w.gmv.3 


# 7. Construct GMV portfolio and its Sharpe ratio

# GMV portfolio
w <- w.gmv.3
gmv_ret.xts <- lr[, "msft"]*w[1] + lr[, "aapl"]*w[2] 
colnames(gmv_ret.xts) <- c("gmv_ret")  # name the column
head(gmv_ret.xts)
tail(gmv_ret.xts) 

# sample mean, sample standard deviation
muhat.port = mean(gmv_ret.xts) 
muhat.port
sigma2hat.port = var(gmv_ret.xts)  
sigma2hat.port
sigmahat.port = sd(gmv_ret.xts)
sigmahat.port

# Or use the formula for mean and variance of portfolio
muhat.port.2 = w[1]*muhat[1] + w[2]*muhat[2]
muhat.port.2 # same as muhat.port above
sigma2hat.port.2 = w[1]^2*sigma2hat[1] + w[2]^2*sigma2hat[2] + 2*w[1]*w[2]*cov.mat[1,2]
sigma2hat.port.2 
sigmahat.port.2 = sqrt(sigma2hat.port.2)
sigmahat.port.2 # same as sigma.port above

# Sharpe ratio 
SR.port = (muhat.port-0.03/12)/sigmahat.port
SR.port












