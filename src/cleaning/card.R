card_dev <- read.delim("../../data/preprocessed/card_dev.csv", sep=";")
card_comp <- read.delim("../../data/preprocessed/card_comp.csv", sep=";")

card <- rbind(card_dev, card_comp)
card$type<-unclass(as.factor(card$type))

disp <- read.delim("../../data/preprocessed/disp.csv", sep=";")
disp$type<-NULL


card_merge<-merge(disp, card, by = "disp_id", all.x = TRUE)

# Add column "has card"
card_merge$has_card <- !is.na(card_merge$card_id)
card_merge$has_card[card_merge$has_card == FALSE] <- 0


card_merge$type[is.na(card_merge$type)] <- 0
card_merge<-rename(card_merge, type_card = type)

# Drop columns
card_merge$issued_date <-NULL
card_merge$card_id<-NULL
card_merge$account_id<-NULL
card_merge$client_id<-NULL

write.csv(card_merge, file="../../data/cleaned/card.csv", row.names = FALSE)
