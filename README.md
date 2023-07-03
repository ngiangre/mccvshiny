# mccvshiny

Interactive App for exploring Monte Carlo Cross Validation predictions from the {mccv} package using Shiny for Python

## Objective

1. Showcase the MCCV algorithm. More details on the algorithm and use cases at [nickg.mccv.bio](nickg.mccv.bio)

2. Provide an online tool for 

   A. Setting and generating univariate prior distributions based on t, beta, and normally distributed data.

   B. Generating MCCV prediction results based on specified univariate data distributions.

   C. Visualizing MCCV prediction results.

3. Opportunity for Nick to learn Shiny for Python

## Components

1. Generate Data

Input: N [0,1000] sample size parameter

A. Normal data: mu [-5,5] and sigma [0,5] parameters

B. Beta data: a [0,5] and b [0,5] parameters

C. T data: mu [-5,5] and df [1,N-1] parameters

Input: R range slider for target class 1 samples

Input: P [0,1] proportion of class 1 samples in target distribution (remainder as class 0 samples)

Output: Dataframe of status | result

Output: Scatter boxplot of univariate distribution colored by class membership

2. Parameterize MCCV Algorithm

Input: Number of Bootstraps [1,200]

Input: Models ['Logistic Regression', 'Random Forest', 'Support Vector Machines', 'Gradient Boosting Classifier']

Output: Dictionary of mccv parameters

3. Run MCCV Algorithm

Create mccv and permuted_mccv objects given parameters and data

Input: Dictionary of mccv parameters

Input: Dataframe of status | result

Output: Two mccv objects

3. Display MCCV Result Tables

Show the four tables as four tabs

4. Display MCCV Result Plots

Show 4 standard plots based on the 4 tables


## Design


## Notes

- Following https://shiny.posit.co/py/docs/comp-r-shiny.html and https://shiny.posit.co/py/docs/install.html closely to get started