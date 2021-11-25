  
  library(dplyr)
  library(ggplot2)
  library(ggpubr)
  
  
  trans<-read.delim("../data/preprocessed/trans_dev.csv", sep=";")
  loan <- read.delim("../data/preprocessed/loan_dev.csv", sep=";")
  loan <- loan[c("account_id", "loan_date", "duration", "amount", "status")]
  
  # MERGE [LOAN, TRANSACTIONS]
  merged <- merge(loan, trans, by="account_id", suffixes=c("_loan", "_trans"))
  merged$trans_day<-NULL
  merged$trans_month<-NULL
  merged$trans_year<-NULL
  
  # To date
  merged$trans_date<-as.Date(merged$trans_date)
  merged$loan_date<-as.Date(merged$loan_date)
  
  # Drop rows with transactions after loan.
  merged<-merged[merged$loan_date > merged$trans_date,]
  
  
  # ANALYSIS AMOUNT TRANS =======================================================
  
  # [FEATURE ENGINEERING] Days before the loan.
  merged$diff_days <- merged$loan_date - merged$trans_date
  merged$diff_month <- as.numeric(floor(merged$diff_days/30)) # Diff month from the loan
  
  # How the balance is related with paying the loan or not? 
  balance_statis <- function(merged, months){
    
    # Removing transactions that happened at least x months before the loan request.
    df<- merged[merged$diff_month < 3, ]

    # Let's check the balance during this period.
    df<-df[c('account_id', 'balance', 'status', 'amount_loan')]
    df<-df %>%
      group_by(account_id, status, amount_loan) %>% 
      summarise(min_balance=min(balance), mean_balance=mean(balance), max_balance = max(balance))
     
    return(df)
  } 
  
# PLOTS ======================================================================
  
df <- balance_statis(merged, 6)
df$status[df$status == -1] <- 2
colors <- adjustcolor(c("red", "green")[df$status])

# Min balance
plot(df$min_balance, df$amount_loan, main="Min balance and loan_amount",
     xlab="Min Balance ", ylab="Loan amount", pch=20, col = colors) 

# Max balance 
plot(df$max_balance, df$amount_loan, main="Max balance and loan_amount",
     xlab="Max Balance ", ylab="Loan amount", pch=20, col = colors) 

# Mean balance
plot(df$mean_balance, df$amount_loan, main="Mean balance and loan_amount",
     xlab="Mean Balance ", ylab="Loan amount", pch=20, col = colors) 



