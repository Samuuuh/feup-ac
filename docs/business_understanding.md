# Business Understanding

## Business Goals

- Lower the percentage of unpaid loans.
- Company with more confidance when making new loans.
- Improve their service by having an accurate prediction if the client can have a loan or not.
- As a measurement of quality, the model here presented must be able to predict correctly at least 7 scenarios out of 10 where the person does not pay the loan. 
- The study finishes on time.

## Requirements Analysis
### User Stories

The application has only one actor, the *User* that can do all the following operations:

- Train models using the selected configurations,
  so that the *User* can choose the models that are going to be used for the other operations

- Compare the scoring of the results of models, 
  so that the *User* can verify the differences of the models and understand the capabilities of each one of them

- Calculate the area under the curve score for the models,
  so that the *User* can use an objective scoring method to compare all the models

- Use a specific model configuration to predict the default results of a dataset,
  so that the *User* can use a chosen model to predict missing default attributes for loans

### Other Requirements

The system should satisfy the following requirements:

- The application should provide a simple and easy to use CLI interface, so people can use it regardless of their programming knowledge
- The project needs to be done before its deadline so that all the desired features are implemented and used in the evaluation of the project
- The application should have two different pipelines, one for development and other for production

## Data Mining Goals

By using __direct data mining__, this project main goal is to __predict__ the probability of a user paying back the loan if the bank allows the lending.     
As mentioned in the business goals, the model here presented must have at least an AUC of 0.7.
Now that the business goal is clear, it's time to translate it into a data mining reality. 

- This is classified as a prediction problem.
- Building a model using available data to predict the likelihood of a person paying back the loan
- Assigning to each loan a probability of it beign left unpaid

These data mining goals, if met, can then be used by the business to reduce the company loss.
