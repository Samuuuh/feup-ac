library(ggplot2)
library(patchwork)

# OUTLIERS ======================================================
# Visualizes boxplot with outliers 
get_outliers_plot <- function(df, field){
  return(ggplot(df, aes_(x="", y=as.name(field))) + geom_boxplot())
} 

# Visualizes the QQPlot for possible values substitutions
show_distribution <- function(df, field){
  print(field)
  ggplot(df, aes_(sample=as.name(field))) + geom_qq(geom='point') +
    stat_qq_line() + ggtitle(field)
}

# Show a table with outliers 
show_table_outliers <- function(df, field){
  outliers <- boxplot.stats(df[[field]])$out
  out_ind <- which(df[[field]] %in% c(outliers))
  df[out_ind, ]
}


show_all_outliers_plot <- function(df){
  patch = c()
  for (i in names(df)){
    patch <- get_outliers_plot(df, i)  + patch
  }
  patch 
}

show_all_distributions_plot <- function(df){
  patch = c()
  for (i in names(df)){
    patch <- show_distribution(df, i)  + patch
  }
  patch 
}

# FEATURE ENGINEERING =========================================
one_hot_encoding <- function(df, name){
  return (df %>% mutate(value=1) %>% spread(name, value, fill=0))
}
