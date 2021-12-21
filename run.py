import os 
from definitions import ROOT_DIR
from methods.main_method.Kmeans_CentroidBase_MMR_SentencePosition import Summarizer
import argparse
from utils.preprocessing import Preprocessing
from tqdm.auto import tqdm 


if __name__ == "__main__":
    root_directory = ROOT_DIR + "/"

    doc_folders = os.listdir(root_directory + "Data/summ/Documents")

    summarizer = Summarizer(n_clusters=10
                            , len_summary=16)

    parser = argparse.ArgumentParser()

    parser.add_argument('--folder_to_save', help='Folder to save summaries')
    args = parser.parse_args()

    folder_to_save = args.folder_to_save
    # path_to_save = root_directory + "Data/summ/" + folder_to_save + "/"
    path_to_save = folder_to_save

    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    progress_bar = tqdm(range(len(doc_folders)))
    progress_bar.set_description("Running: ")
    for folder in doc_folders:
        path = os.path.join(root_directory,"Data", "summ", "Documents", folder)

        sentences, last_indexs = Preprocessing().openDirectory(path)
        text_sents = []
        for item in sentences:
            text_sents.append(item.getStemmedWords())

        clean_sents = []
        org_sents = []
        for item in sentences:
            org_sents.append(item.getOGwords())

            tmp = ""
            for word in item.getStemmedWords():
                tmp += word + " "

            if tmp[-1] not in clean_sents:
                clean_sents.append(tmp[:-1])

        progress_bar.set_postfix_str(f'Processing {path} with n_sents={len(text_sents)}')
        summary = summarizer.summary(sentences, text_sents, org_sents, last_indexs)

        path = os.path.join(path_to_save, f"{folder}.txt")
        with open(path, 'w', encoding='utf-8') as fileOut:
            fileOut.write("\n".join(summary))

        progress_bar.update(1)

    progress_bar.close()