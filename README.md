
# **AI Capstone Project**

This repository contains a comprehensive workflow for data scraping, synthetic data generation, and fine-tuning a LLaMA 3.1 model using synthetic data. The project leverages state-of-the-art tools to build and fine-tune large language models for advanced applications.

---

## **Project Workflow**

### **1. Data Scraping**
- **File:** `scraper.py`
- **Description:** 
  - This script scrapes data from **Sofifs**, a platform for high-quality data collection. 
  - Outputs a raw dataset ready for preprocessing and synthetic data generation.

---

### **2. Synthetic Data Generation**
- **File:** `data.ipynb`
- **Description:** 
  - Uses **LLaMA 3.1** via the **Ollama** framework to generate synthetic data.
  - Processes and formats the scraped data to create a high-quality synthetic dataset.
  - Provides exploratory data analysis (EDA) and pre-generation sanity checks.

---

### **3. Model Fine-Tuning**
- **File:** `model_fine_tunning.py`
- **Description:** 
  - Fine-tunes the **LLaMA 3.1 8-billion parameter model** with the synthetic dataset.
  - Implements optimized training strategies for efficient large-model training.
  - Produces a fine-tuned model ready for downstream tasks.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/YourUsername/AI_Capstone.git
cd AI_Capstone
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```
Ensure that your environment has the following:
- Python 3.8 or higher
- GPU support (e.g., NVIDIA CUDA for LLaMA fine-tuning)

### **3. Run the Workflow**
1. **Data Scraping**:
   ```bash
   python scraper.py
   ```
2. **Synthetic Data Generation**:
   Open `data.ipynb` in Jupyter Notebook and execute the cells.
3. **Model Fine-Tuning**:
   ```bash
   python model_fine_tunning.py
   ```

---

## **Technologies Used**
- **Programming Languages**: Python
- **Frameworks**: 
  - Ollama for synthetic data generation
  - PyTorch for model fine-tuning
- **Model**: LLaMA 3.1 (8-billion parameters)

---

## **Directory Structure**
```
.
├── scraper.py              # Script for data scraping
├── data.ipynb              # Notebook for synthetic data generation
├── model_fine_tunning.py   # Script for model fine-tuning
├── requirements.txt        # Required Python libraries
├── README.md               # Project documentation
├── tmp/                    # Temporary files (ignored in Git)
├── app.py                  #chat interface to interact with out Scouting Agent
```

---

## **Future Enhancements**
- Add support for multi-GPU fine-tuning.
- Expand data scraping to include multiple sources.
- Integrate evaluation metrics for fine-tuned models.

---

## **Contact**
For queries or collaboration, please contact:
**Venkata Sai Aswath Duvvuru**  
[Your Email] | [Your LinkedIn]  

---
