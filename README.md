# studious-journey
My first project! An end-to-end Credit Risk Scorecard using WoE &amp; Logistic Regression. It includes a Streamlit web app that calculates real-time credit scores for instant loan approvals/declines.
# 📊 Credit Risk Scorecard & Streamlit App

An end-to-end Credit Risk Scorecard model using Weight of Evidence (WoE) and Logistic Regression. This project includes a Streamlit web application that calculates real-time credit scores to provide instant loan approval or decline decisions based on applicant financial data.

## 🚀 Features

* **Statistical Modeling:** Built using traditional banking risk methodologies, utilizing WoE transformations to bin continuous variables and Logistic Regression to scale probabilities into a standard scorecard format.
* **Dynamic Scoring Engine:** Reads model rules and points dynamically from a JSON configuration file (`scorecard_config.json`).
* **Interactive Web App:** A user-friendly Streamlit frontend that takes applicant inputs (Age, Monthly Income, Revolving Utilization) and instantly outputs a final credit score and decision.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Frontend:** Streamlit
* **Modeling (Backend):** Scikit-Learn, Pandas, NumPy (for initial training and WoE binning)
* **Configuration:** JSON (Artifact deployment)

## 📂 Project Structure

```text
├── artifacts/
│   ├── app.py                   # The Streamlit web application script
│   └── scorecard_config.json    # The deployed model parameters, bin edges, and scorecard points
├── README.md                    # Project documentation
