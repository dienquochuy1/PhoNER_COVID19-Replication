# main.py
from ner_model import COVID_NER_AzureOpenAI
from utils import load_data

TEST_DATA_PATH = 'D:\\NER_CODE\\covid_ner_project\\PhoNER_COVID19\\data\\word\\test_word.json'

def main():
    test_data = load_data(TEST_DATA_PATH)
    
    # Toggle features here
    ner_system = COVID_NER_AzureOpenAI(
        use_decomposed=False,  # Enable Decomposed-QA
        use_syntactic_prompting=True,  # Enable syntactic prompting 
        use_tool_augmentation=False,  # Enable tool augmentation
        sc_samples=1  # Self-consistency samples (1 to disable)
    )
    
    f1, report = ner_system.evaluate(test_data[:1000])
    
    with open('ner_results.txt', 'w', encoding='utf-8') as f:
        f.write(f"F1 Score: {f1:.4f}\n")
        f.write(report)

if __name__ == "__main__":
    main()