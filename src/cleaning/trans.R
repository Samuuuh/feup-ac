
library(dplyr)
library(ggplot2)
library(ggpubr)

# Train
trans<-read.delim("../../data/preprocessed/trans_dev.csv", sep=";")
loan <- read.delim("../../data/preprocessed/loan_dev.csv", sep=";")
loan <- loan[c("account_id", "loan_date", "duration", "amount", "status")]

# Test
trans_comp<-read.delim("../../data/preprocessed/trans_comp.csv", sep=";")
loan_comp <- read.delim("../../data/preprocessed/loan_comp.csv", sep=";")
loan_comp <- loan_comp[c("account_id", "loan_date", "duration", "amount", "status")]


# MERGE [LOAN, TRANSACTIONS] =================================================

merged <- merge(loan, trans, by="account_id", suffixes=c("_loan", "_trans"))
merged$trans_day<-NULL
merged$trans_month<-NULL
merged$trans_year<-NULL

# To date
merged$trans_date<-as.Date(merged$trans_date)
merged$loan_date<-as.Date(merged$loan_date)

# Drop rows with transactions after loan.
merged<-merged[merged$loan_date > merged$trans_date,]


# TREAT DATA =================================================================

treat_data <- function(df){
  df$operation[df$operation == "nan"]<-"other"
  df$k_symbol[df$k_symbol == ""]<-"other"
  df$bank[df$bank == ""]<-"other"
  
  return(df)
}

trans <-treat_data(trans)
trans_comp<-treat_data(trans_comp)

ggplot(trans, aes(x=trans$operation)) + geom_bar() + ggtitle("Operations count")


# FEATURE ENGINEERING ========================================================

# 1) Bank accounts with only nan accounts.

# 1.1) Build
  merged$account[is.na(merged$account)] <-0
  merged$is_na <-merged$account == 0
  
  # ??
  counter<-merged %>%
    group_by(account_id, status) %>%
    summarise(only_na_account=min(is_na))

# 1.2) Study
  counter %>%
    group_by(only_na_account) %>% 
    count(status)
  

# 1.3) Application
  apply_nan_acc <- function(df){
    # Treat data
    df$account[is.na(df$account)] <-0
    df$is_na <-df$account == 0
    
    only_na_table<-df %>%
      group_by(account_id) %>%
      summarise(only_na_account=min(is_na))
    
    df <- merge(df, only_na_table, by="account_id")
    return (df)
  }
  
  trans<-apply_nan_acc(trans)
  trans_comp<-apply_nan_acc(trans_comp)
  

# 2) Min, max and mean balance in the last M months
  

# 2.1) Build
  
  merged$diff_days <- merged$loan_date - merged$trans_date
  merged$diff_month <- as.numeric(floor(merged$diff_days/30)) # Diff month from the loan
  
  # How the balance is related with paying the loan or not? 
  balance_status <- function(merged, months){
    
    # Removing transactions that happened at least x months before the loan request.
    df<- merged[merged$diff_month < months, ]
    
    # Let's check the balance during this period.
    df<-df[c('account_id', 'balance', 'status', 'amount_loan')]
    df<-df %>%
      group_by(account_id, status, amount_loan) %>% 
      summarise(min_balance=min(balance), mean_balance=mean(balance), max_balance = max(balance))
    
    return(df)
  } 
  
# 2.2) Study

  df <- balance_status(merged, 6)
  df$status[df$status == -1] = 2
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
  

  # Important variable for trees
  cor.test(df$min_balance, df$status, method=c("pearson"))
  
# 2.2) Application
  
  apply_balance <- function(l, t, m){
    temp <- merge(l, t, by="account_id", suffixes=c("_loan", "_trans"))
    
    temp$trans_date<-as.Date(temp$trans_date)
    temp$loan_date<-as.Date(temp$loan_date)
    
    # Drop rows with transactions after loan.
    temp<-temp[temp$loan_date > temp$trans_date,]
    
    temp$diff_days <- temp$loan_date - temp$trans_date
    temp$diff_month <- as.numeric(floor(temp$diff_days/30)) # Diff month from the loan
    
    # Removing transactions that happened at least x months before the loan request.
    temp<- temp[merged$diff_month < m, ]
    
    # Let's check the balance during this period.
    temp<-temp[c('account_id', 'balance', 'only_na_account')]
    temp<-temp %>%
      group_by(account_id, only_na_account) %>% 
      summarise(min_balance=min(balance), mean_balance=mean(balance), max_balance = max(balance))
    
    temp <- merge(temp, t, by="account_id")
    return (temp)
  }
  
  trans<-apply_balance(trans,loan, 6)
  trans_comp<-apply_balance(trans_comp,loan_comp, 6)
  
  clean_data<-function(df){
    # From the merge
    df$status<-NULL
    df$loan_date<-NULL
    df$duration<-NULL
    df$amount_loan<-NULL
    return (df)
  }

  trans_comp<-clean_data(trans_comp)
  trans<-clean_data(trans)

  trans$amount <- NULL
  trans_comp$amount <-NULL
  

write.csv(trans, file="../../data/cleaned/trans_dev.csv", row.names = FALSE)
write.csv(trans_comp, file="../../data/cleaned/trans_comp.csv", row.names = FALSE)
