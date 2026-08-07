correlogram <- function(x,
                        max.lag   = 40,
                        fit       = NULL,        # optional model object (lm, arima, etc.)
                        ci.level  = 0.95,
                        bar.width = 0.2,
                        main.acf  = NULL) {
  
  # --------- Helper: infer number of estimated parameters from fit ----------
  adj <- 0
  if (!is.null(fit)) {
    cf <- try(stats::coef(fit), silent = TRUE)
    if (!inherits(cf, "try-error") && !is.null(cf)) {
      adj <- length(cf)
    }
  }
  
  # --------- Clean & coerce input ----------
  x <- na.omit(x)
  
  if (is.matrix(x) || is.data.frame(x)) {
    if (ncol(x) != 1) stop("x must be a univariate series (one column).")
    x <- x[, 1]
  }
  
  x <- as.numeric(x)
  n <- length(x)
  
  if (n < 5) stop("Not enough observations after removing NA values.")
  
  if (max.lag > (n - 1)) {
    max.lag <- n - 1
    warning("max.lag reduced to n-1 because series is short.")
  }
  
  # --------- ACF (lags 1..max.lag only) ----------
  ac_all <- stats::acf(x, lag.max = max.lag, plot = FALSE)$acf
  ac_pos <- as.numeric(ac_all[-1])  # lags 1..max.lag
  lags   <- 1:max.lag
  
  # --------- Ljung–Box Q-stat & Prob with df adjustment ----------
  Q    <- numeric(max.lag)
  Prob <- numeric(max.lag)
  
  for (k in 1:max.lag) {
    rho_k <- ac_pos[1:k]
    Q[k]  <- n * (n + 2) * sum(rho_k^2 / (n - (1:k)))
    
    df <- k - adj
    df <- max(1, df)  # avoid df <= 0
    Prob[k] <- stats::pchisq(Q[k], df = df, lower.tail = FALSE)
  }
  
  # --------- Output table ----------
  corr_tab <- data.frame(
    Lag  = lags,
    AC   = round(ac_pos, 4),
    Q    = round(Q,      4),
    Prob = signif(Prob,  4)
  )
  
  print(corr_tab, row.names = FALSE)
  
  # --------- Common confidence band ----------
  ci <- stats::qnorm((1 + ci.level) / 2) / sqrt(n)
  
  # --------- Plot ACF ----------
  if (is.null(main.acf)) main.acf <- "ACF (Correlogram)"
  
  ylim <- c(min(ac_pos, -ci) * 1.2, max(ac_pos, ci) * 1.2)
  
  plot(lags, ac_pos, type = "n",
       ylim = ylim,
       xlab = "Lag", ylab = "ACF",
       main = main.acf,
       xaxt = "n")
  
  x_ticks <- c(1, seq(5, max(lags), by = 5))
  x_ticks <- x_ticks[x_ticks <= max(lags)]
  axis(1, at = x_ticks, labels = x_ticks)
  
  abline(h = 0, col = "gray50")
  abline(h = c(-ci, ci), lty = 2, col = "red")
  
  cols <- ifelse(ac_pos >= 0, "steelblue", "orange")
  for (i in seq_along(lags)) {
    x0 <- lags[i] - bar.width
    x1 <- lags[i] + bar.width
    y0 <- 0
    y1 <- ac_pos[i]
    if (y1 >= 0) rect(x0, y0, x1, y1, col = cols[i], border = cols[i])
    else         rect(x0, y1, x1, y0, col = cols[i], border = cols[i])
  }
  
  invisible(corr_tab)
}
