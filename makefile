PYTHON = python
R = Rscript 

.PHONY: all clean preprocess_ clean_



r_filepath = ./src/cleaning/
r_files = card.R client.R disp.R district.R trans.R 
r_executables = $(addprefix $(r_filepath), $(r_files))

all: preprocess_ clean_ 

preprocess_:
	@echo "Generating preprocessed files..." 
	$(PYTHON) -m src.preprocessing

clean_: 
	for file in $(r_executables); do \
		$(R) $$file ; \
	done

submit_:
	$(PYTHON) -m src


clean:
	@echo "Removing preprocessed files"
	@rm -r ./data/preprocessed/*
	@echo "Removing cleaned"
	@rm -r ./data/cleaned/*

