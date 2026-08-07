
library(quantmod)



#========================================================
# 1. Choose sample period
#========================================================
start_date <- "2015-12-01"
end_date   <- "2025-12-31"

#========================================================
# 2. Vanguard ETFs in the 3x3 style box
#    Order rows as: Small, Mid, Large
#========================================================
tickers <- c("VBK", "VB", "VBR",   # Small: growth, blend, value
             "VOT", "VO", "VOE",   # Mid:   growth, blend, value
             "VUG", "VV", "VTV")   # Large: growth, blend, value

#========================================================
# 3. Download ETF data from Yahoo Finance
#========================================================
getSymbols(tickers, src = "yahoo", from = start_date, to = end_date)


vbk.m.p = to.monthly(VBK$VBK.Adjusted, OHLC = FALSE)
vb.m.p  = to.monthly(VB$VB.Adjusted, OHLC = FALSE)
vbr.m.p = to.monthly(VBR$VBR.Adjusted, OHLC = FALSE)

vot.m.p = to.monthly(VOT$VOT.Adjusted, OHLC = FALSE)
vo.m.p  = to.monthly(VO$VO.Adjusted, OHLC = FALSE)
voe.m.p = to.monthly(VOE$VOE.Adjusted, OHLC = FALSE)

vug.m.p = to.monthly(VUG$VUG.Adjusted, OHLC = FALSE)
vv.m.p  = to.monthly(VV$VV.Adjusted, OHLC = FALSE)
vtv.m.p = to.monthly(VTV$VTV.Adjusted, OHLC = FALSE)


m.p <- merge(vbk.m.p, vb.m.p, vbr.m.p,
             vot.m.p, vo.m.p, voe.m.p,
             vug.m.p, vv.m.p, vtv.m.p)

colnames(m.p) <- c("VBK", "VB", "VBR",
                   "VOT", "VO", "VOE",
                   "VUG", "VV", "VTV")


# Optional - export to Excel
# m.prices.df <- data.frame(
#   Date = format(as.Date(index(m.p)), "%Y-%m"),
#   coredata(m.p),
#   row.names = NULL
# )
# head(m.prices.df)
# 
# writexl::write_xlsx(m.prices.df, "W6_Vanguard_MPrices.xlsx")
# end Optional





# Log Returns
m.lr.p = na.omit(diff(log(m.p)))*100
# sample mean
mean_vec_lr <- colMeans(m.lr.p)

#========================================================
# 3x3 style box: mean monthly log return (%)
#========================================================

mean_box_lr <- matrix(mean_vec_lr,
                      nrow = 3, byrow = TRUE,
                      dimnames = list(c("Small", "Mid", "Large"),
                                      c("Growth", "Blend", "Value")))


mean_box_lr <- round(mean_box_lr, 3)
cat("\n3x3 Style Box: Mean Monthly Lor Return (%)\n")
mean_box_lr


#========================================================
# VALUE AT RISK (VaR) - Historical Method
#========================================================
# 95% confidence level, 1-month horizon
confidence <- 0.95

var_vec <- apply(m.lr.p, 2, function(etf) {
  -quantile(etf, probs = 1 - confidence)  # negative so VaR is expressed as a positive loss
})

# 3x3 style box: VaR
var_box <- matrix(var_vec,
                  nrow = 3, byrow = TRUE,
                  dimnames = list(c("Small", "Mid", "Large"),
                                  c("Growth", "Blend", "Value")))
var_box <- round(var_box, 3)
cat("\n3x3 Style Box: Historical VaR 95% Monthly Log Return (%)\n")
var_box