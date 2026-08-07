
y.df <- readxl::read_excel("Week 8 q3.xlsx")   

library(xts)
y.xts <- as.xts(y.df)


fit_ar1 <- arima(y.xts, order = c(1, 0, 0), include.mean = TRUE)
fit_ar2 <- arima(y.xts, order = c(2, 0, 0), include.mean = TRUE)
fit_ar3 <- arima(y.xts, order = c(3, 0, 0), include.mean = TRUE)
fit_ar4 <- arima(y.xts, order = c(4, 0, 0), include.mean = TRUE)
fit_ar5 <- arima(y.xts, order = c(5, 0, 0), include.mean = TRUE)

fit_ar1
fit_ar2
fit_ar3
fit_ar4
fit_ar5


# optional

aic_table <- data.frame(
  Model = c("AR(1)", "AR(2)", "AR(3)", "AR(4)", "AR(5)"),
  AIC = c(
    fit_ar1$aic,
    fit_ar2$aic,
    fit_ar3$aic,
    fit_ar4$aic,
    fit_ar5$aic
  )
)

aic_table

aic_table[order(aic_table$AIC), ]

source("Correlogram.R")
resid = residuals(fit_ar3)
correlogram(resid, max.lag = 10, main = "Residuals AR(3)")

