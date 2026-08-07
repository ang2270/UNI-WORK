# Question 1

library(quantmod)
options("getSymbols.warning4.0"=FALSE)
getSymbols(Symbols = c("MSFT" ), from="2015-12-01", to="2025-12-31",
           auto.assign=TRUE, warnings=FALSE)

# convert to monthly
msft_M_P = to.monthly(MSFT$MSFT.Adjusted, OHLC=FALSE) 

# log return
lr = na.omit(diff(log(msft_M_P)))
colnames(lr) <- c("msft")
head(lr)  
tail(lr)


# download from Ken French's website
library(frenchdata)
ff3 <- download_french_data("Fama/French 3 Factors")
ff3_monthly_raw <- ff3$subsets$data[[1]] 

# convert to xts object
library(xts) 
ff3_monthly_raw$date <- as.yearmon(as.character(ff3_monthly_raw$date), format = "%Y%m")
ff3_xts <- xts(
  ff3_monthly_raw[, c("Mkt-RF","SMB","HML","RF")] ,   # drop the date column
  order.by = as.Date(ff3_monthly_raw$date)                 # month index
)
colnames(ff3_xts) <- c("mkt_excess","smb","hml","rf")
head(ff3_xts)
# convert to "year-month" (no date) 
index(ff3_xts) <- as.yearmon(index(ff3_xts))  
head(ff3_xts)
tail(ff3_xts)


##########################
# Note: Ken French's dataset
# RF is in %
# mkt_excess is in %

lr = lr*100 # log return is now in %


#########################
# sub-periods
#########################

# sub-period 1
lr.p1 = lr["2016-01/2020-12"]
head(lr.p1)
tail(lr.p1)

ff3.p1 = ff3_xts["2016-01/2020-12"]
head(ff3.p1)
tail(ff3.p1)

# sub-period 2
lr.p2 = lr["2021-01/2025-12"]
head(lr.p2)
tail(lr.p2)

ff3.p2 = ff3_xts["2021-01/2025-12"]
head(ff3.p2)
tail(ff3.p2)



#---------------------
# capm period 1
capm.msft.p1 <- lm(lr$msft-ff3.p1$rf~ff3.p1$mkt_excess)
summary(capm.msft.p1) 


# capm period 2
capm.msft.p2 <- lm(lr$msft-ff3.p2$rf~ff3.p2$mkt_excess)
summary(capm.msft.p2) 

# Question 2


library(frenchdata)


#########################################
# (a) "Fama/French 3 Factors" Monthly
#########################################

ff3 <- download_french_data("Fama/French 3 Factors")

ff3_monthly_raw <- ff3$subsets$data[[1]] 

# convert to xts object 
library(xts) 
# if date is like 192607, 202312, etc.
ff3_monthly_raw$date <- as.yearmon(as.character(ff3_monthly_raw$date), format = "%Y%m")
ff3.xts <- xts(
  ff3_monthly_raw[, c("Mkt-RF","SMB","HML","RF")] ,   # drop the date column
  order.by = as.Date(ff3_monthly_raw$date)            # month index
)
head(ff3.xts)

# Optional: Rename the columns
colnames(ff3.xts) <- c("mkt_excess","smb","hml","rf") 
head(ff3.xts)

# convert from "1926-07-01" to "Jul 1926" 
index(ff3.xts) <- as.yearmon(index(ff3.xts))  
head(ff3.xts)
tail(ff3.xts)



#########################################
# (b) "5 Industry Portfolios"
#########################################

# Download the dataset (exact name on Ken French's library)
ind5 <- download_french_data("5 Industry Portfolios")

# Grab the "Average Value Weighted Returns -- Monthly"
id5.df <- ind5$subsets$data[[1]] 
head(id5.df)

# convert to xts
library(xts) 
id5.df$date <- as.yearmon(as.character(id5.df$date), format = "%Y%m")
id5.xts <- xts(
  id5.df[, c("Cnsmr","Manuf","HiTec","Hlth","Other")] ,   # drop the date column
  order.by = as.Date(id5.df$date)                 # month index
)
head(id5.xts)

# convert from "1926-07-01" to "Jul 1926" 
index(id5.xts) <- as.yearmon(index(id5.xts))  # match by year-month
head(id5.xts)
tail(id5.xts)


#####################################
# (c) Momentum Factor (Mom)
####################################


# 1) Download the dataset (exact name on Ken French's library)
mom_raw <- download_french_data("Momentum Factor (Mom)")

# 2) Grab [[1]] monthly 
mom_raw.df <- mom_raw$subsets$data[[1]] 
head(mom_raw.df)


# convert to xts
library(xts) 
mom_raw.df$date <- as.yearmon(as.character(mom_raw.df$date), format = "%Y%m")
mom.xts <- xts(
  mom_raw.df[, "Mom" ],   # drop the date column
  order.by = as.Date(mom_raw.df$date)                 # month index
)
head(mom.xts)
# convert from "1926-07-01" to "Jul 1926" 
index(mom.xts) <- as.yearmon(index(mom.xts))  # match by year-month
head(mom.xts)




#############################
# January 1997 to December 2025

id5.xts <- id5.xts["1997-01/2025-12"]
head(id5.xts)
tail(id5.xts)

ff3.xts <- ff3.xts["1997-01/2025-12"]
head(ff3.xts)
tail(ff3.xts)

mom.xts <- mom.xts["1997-01/2025-12"]
head(mom.xts)
tail(mom.xts)

# restricted capm
capm.fit <- lm(id5.xts$Cnsmr-ff3.xts$rf~ff3.xts$mkt_excess)
summary(capm.fit)

# unrestricted multi-factor
multi.fit <- lm(id5.xts$Cnsmr-ff3.xts$rf~ff3.xts$mkt_excess+ff3.xts$smb+ff3.xts$hml+mom.xts)
summary(multi.fit)










