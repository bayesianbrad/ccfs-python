import numpy as np
from utils.commonUtils import is_numeric

def treeOutputsToForestPredicts(CCF, treeOutputs):
    """
    Converts outputs from individual trees to forest predctions and
    probabilities.

    Parameters
    ----------
    CCF = Output of genCCF
    treeOutputs = Array typically generated by predictCCF. Description provided
                  in doc string of predictCCF as it is provided as an output.
    """
    if CCF["bReg"]:
        forestPredicts = np.squeeze(np.mean(treeOutputs, axis=1))
        forestProbs = [];
    else:
        forestProbs = np.squeeze(np.mean(treeOutputs, axis=1))

        if CCF["options"]["bSepPred"]:
            forestPredicts = forestProbs > 0.5
        else:
            forestPredicts = np.empty((forestProbs.shape[0], CCF["options"]["task_ids"].size))
            forestPredicts.fill(np.nan)

            for nO in range ((CCF["options"]["task_ids"].size)-1):
                forestPredicts[:, nO] = np.argmax(forestProbs[:, CCF["options"]["task_ids"][nO]:(CCF["options"]["task_ids"][nO+1]-1)], axis=1)
            forestPredicts[:, -1] = np.argmax(forestProbs[:, CCF["options"]["task_ids"][-1]:], axis=1)

        if is_numeric(CCF["classNames"]):
            if islogical(forestPredicts):
                assert (forestPredicts.shape[1] == 1), 'Class names should have been a cell if multiple outputs!'
                forestPredicts = CCF["classNames"][forestPredicts+1]
            else:
                forestPredicts = CCF["classNames"][forestPredicts]
        # Fix needed
        elif isinstance(CCF["classNames"], pd.DataFrame) and np.any(cellfun(@(x) is_numeric(x) and x.size > 1, CCF["classNames"])):
            assert (CCF["classNames"].size == forestPredicts.shape[1]), 'Number of predicts does not match the number of outputs in classNames'

    return forestPredicts, forestProbs