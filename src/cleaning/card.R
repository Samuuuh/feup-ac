library("plyr")
library(RSQLite)
library(DBI)

con_comp <- dbConnect(RSQLite::SQLite(), "data/ac-comp_v-1.db")
con_dev <- dbConnect(RSQLite::SQLite(), "data/ac-dev_v-1.db")

card_dev <- dbGetQuery(con_dev, "SELECT * FROM card")
card_comp <- dbGetQuery(con_comp, "SELECT * FROM card")
card <- rbind(card_dev, card_comp)

disp <- dbGetQuery(con_comp, "SELECT * FROM disp")
disp$type<-NULL # Removing conflicts between card and disp.
card_merge<-merge(disp, card, by = "disp_id", all.x = TRUE)

# Trating type_card
card_merge<-rename(card_merge, c("type" = "type_card"))
card_merge$type_card[is.na(card_merge$type_card)] <- "other"

# ONE HOT ENCONDING SIMULATION =================================
# Create is junior
card_merge$is_junior[card_merge$type_card == "junior"] <- 1
card_merge$is_junior[card_merge$type_card != "junior"] <- 0

# Create is gold
card_merge$is_gold[card_merge$type_card == "gold"] <- 1
card_merge$is_gold[card_merge$type_card != "gold"] <- 0

#Create is classic
card_merge$is_classic[card_merge$type_card == "classic"] <- 1
card_merge$is_classic[card_merge$type_card != "classic"] <- 0

# OTHER VARIABLES =============================================
# Add column "has card"
card_merge$has_card <- !is.na(card_merge$card_id)
card_merge$has_card[card_merge$has_card == FALSE] <- 0

# Drop columns
card_merge$issued_date <-NULL
card_merge$card_id<-NULL
card_merge$account_id<-NULL
card_merge$client_id<-NULL

write.csv(card_merge, file="data/cleaned/card.csv", row.names = FALSE)
