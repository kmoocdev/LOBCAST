import os
import sys
import torch

# preamble needed for cluster
module_path = os.path.abspath(os.getcwd())
if module_path not in sys.path:
    sys.path.append(module_path)

from src.config import Configuration
import src.constants as cst
from src.main_single import *
from src.main_helper import pick_dataset, pick_model
from src.models.model_executor import NNEngine

kset, mset = cst.FI_Horizons, cst.Models
seed = 0
stock_dataset = "FI"
src_data = "data/saved_models/IODIVENTOPAZZO/"
dirs = [d + '/' for d in os.listdir(src_data) if not d.startswith('.')]

skip = [cst.Models.ATNBoF, cst.Models.AXIALLOB, cst.Models.CNN1, cst.Models.CNN2, cst.Models.CNNLSTM, cst.Models.DAIN, cst.Models.TRANSLOB]
def launch_test(cf: Configuration):

    for k in kset:

        for model in mset:
            if model in skip:
                continue
            print()
            print(model, k)

            cf.CHOSEN_MODEL = model
            cf.HYPER_PARAMETERS[cst.LearningHyperParameter.FI_HORIZON] = k.value

            dir_name = "model={}-seed={}-trst={}-test={}-data={}-peri={}-bw={}-fw={}-fiw={}/".format(
                cf.CHOSEN_MODEL.name,
                cf.SEED,
                cf.CHOSEN_STOCKS[cst.STK_OPEN.TRAIN].name,
                cf.CHOSEN_STOCKS[cst.STK_OPEN.TEST].name,
                cf.CHOSEN_DATASET.value,
                cf.CHOSEN_PERIOD.name,
                cf.HYPER_PARAMETERS[cst.LearningHyperParameter.BACKWARD_WINDOW],
                cf.HYPER_PARAMETERS[cst.LearningHyperParameter.FORWARD_WINDOW],
                cf.HYPER_PARAMETERS[cst.LearningHyperParameter.FI_HORIZON],
            )

            files = [f for f in os.listdir(src_data + dir_name) if not f.startswith('.')]
            assert len(files) == 1, 'We expect that in the folder there is only the checkpoint with the highest F1-score'
            file_name = files[0]

            model_params = HP_DICT_MODEL[cf.CHOSEN_MODEL].fixed_fi
            for param in cst.LearningHyperParameter:
                if param.value in model_params:
                    cf.HYPER_PARAMETERS[param] = model_params[param.value]

            datamodule = pick_dataset(cf)
            model = pick_model(cf, datamodule)
            trainer = Trainer(accelerator=cst.DEVICE_TYPE, devices=cst.NUM_GPUS)

            checkpoint_file_path = src_data + dir_name + file_name
            trainer.test(model=model, datamodule=datamodule, ckpt_path=checkpoint_file_path)

            cf.METRICS_JSON.close(cst.DIR_FI_FINAL_JSONS)



if __name__ == "__main__":

    cf = set_configuration()
    set_seeds(cf)

    cf.CHOSEN_DATASET = cst.DatasetFamily.FI
    cf.CHOSEN_STOCKS[cst.STK_OPEN.TRAIN] = cst.Stocks.FI
    cf.CHOSEN_STOCKS[cst.STK_OPEN.TEST] = cst.Stocks.FI
    cf.CHOSEN_PERIOD = cst.Periods.FI
    cf.IS_WANDB = 0
    cf.IS_TUNE_H_PARAMS = False

    launch_test(cf)


