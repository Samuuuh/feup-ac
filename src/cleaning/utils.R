library(ggplot2)
library(patchwork) 

# GRAPHS ========================================================
show_distribution <- function(df, field, xlabel){
  ggplot(df, aes(x=as.name(field)) + geom_histogram())
}

# OUTLIERS ======================================================
# Visualizes boxplot with outliers 
get_outliers_plot <- function(df, field){
  return(ggplot(df, aes_(x="", y=as.name(field))) + geom_boxplot())
} 

# Visualizes the QQPlot for possible values substitutions
show_qqplot <- function(df, field){
  ggplot(df, aes_(sample=as.name(field))) + geom_qq(geom='point') +
    stat_qq_line() + ggtitle(field)
}

# Show a table with outliers 
show_table_outliers <- function(df, field){
  outliers <- boxplot.stats(df[[field]])$out
  out_ind <- which(df[[field]] %in% c(outliers)) 
  print("OUTLIERS TABLE ========================")
  df[out_ind, ]
}

# Shows all outliers in a plot.
show_all_outliers_plot <- function(df){
  patch = c()
  for (i in names(df)){
    patch <- get_outliers_plot(df, i)  + patch
  }
  patch 
}

# Shows the table distribution
show_all_distributions_plot <- function(df){
  patch = c()
  for (i in names(df)){
    patch <- show_qqplot(df, i)  + patch
  }
  patch 
}

# REPLACE BY QUANTILE =========================================

replace_by_quantile <- function(df, field){
  quantile<-quantile(df[[field]], probs = c(0.50), na.rm = TRUE)
  df[[field]][is.na(df[[field]])] <- quantile  
  return(df)
}


# FEATURE ENGINEERING =========================================
one_hot_encoding <- function(df, name){
  return (df %>% mutate(value=1) %>% spread(name, value, fill=0))
}
