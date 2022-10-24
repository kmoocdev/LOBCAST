
import src.config as co

sweep_configuration_mlp = {
    'method': 'bayes',
    'name': 'sweep',

    'metric': {'goal': 'maximize',
               'name': co.ModelSteps.VALIDATION.value + co.Metrics.F1.value},

    'parameters': {co.TuningVars.BACKWARD_WINDOW.value:  {'values': [  # co.WinSize.SEC10.value,
                                                                     # co.WinSize.SEC20.value,
                                                                     co.WinSize.SEC50.value,
                                                                     # co.WinSize.SEC100.value
                                                                     ]},

                   # co.TuningVars.FORWARD_WINDOW.value:   {'values': [co.WinSize.SEC10.value,
                   #                                                   co.WinSize.SEC30.value,
                   #                                                   co.WinSize.MIN01.value,
                   #                                                   co.WinSize.MIN05.value]},

                   # co.TuningVars.LABELING_THRESHOLD.value: {'min': 0.0005, 'max': 0.005},
                   co.TuningVars.LABELING_SIGMA_SCALER.value: {'max': 1.0, 'min': 0.6},

                   # co.TuningVars.EPOCHS.value:           {'values': [5, 10, 15]},
                   co.TuningVars.LEARNING_RATE.value:      {"values": [0.00018]},  # 'max': 0.001, 'min': 0.0001
                   co.TuningVars.BATCH_SIZE.value:         {'values': [32]},       # [32, 64, 128]
                   co.TuningVars.MLP_HIDDEN.value:         {'values': [200]},
                   co.TuningVars.IS_SHUFFLE.value:         {'values': [True]}
                   }
}
