from pathlib import Path
from datetime import date as datetime_date

from catboost import CatBoostClassifier
import pandas as pd

from credit.models import FizClient


MODEL_PATH = Path(__file__).resolve().parent / "fiz_litza_model.cbm"


def divide_by_ppp(dividend: float | None):
    ppp = 29.06
    if dividend is not None:
        dividend=dividend/ppp
    return dividend


def check_if_credible_fiz_client(
    fiz_client: FizClient,
    int_rate: float,
    funded_amnt: float,
    term: int,
    date: datetime_date,
) -> bool:
    try:
        #Сведения по кредиту
        funded_amnt = divide_by_ppp(funded_amnt)
        issue_y: int = date.year
        issue_m: int = date.month

        #nullable сведения о заёмщике    
        dti=fiz_client.dti
        revol_bal=divide_by_ppp(fiz_client.revolbal)
        mths_since_recent_bc=fiz_client.mthssincerecentbc
        bc_util=fiz_client.bcutil
        revol_util=fiz_client.revolutil
        
        #Non-nullable сведения о заёмщике
        annual_inc=divide_by_ppp(fiz_client.annualinc)
        avg_cur_bal=divide_by_ppp(fiz_client.avgcurbal)
        total_acc=fiz_client.totalacc
        acc_open_past_24mths=fiz_client.accopenpast24mths
        total_bc_limit=divide_by_ppp(fiz_client.totalbclimit)
        total_il_high_credit_limit=divide_by_ppp(fiz_client.totalilhighcreditlimit)
        total_rev_hi_lim=divide_by_ppp(fiz_client.totalilrevhilim)
        emp_length=min(fiz_client.emplength,11)    
        total_bal_ex_mort=divide_by_ppp(fiz_client.totalbalexmort)
        bc_open_to_buy=divide_by_ppp(fiz_client.bcopentobuy)

        df = pd.DataFrame({
            'funded_amnt': [funded_amnt],
            'int_rate': [int_rate],
            'term': [term],
            'issue_y': [issue_y],
            'issue_m': [issue_m],
            'dti': [dti],
            'revol_bal': [revol_bal],
            'mths_since_recent_bc': [mths_since_recent_bc],
            'bc_util': [bc_util],
            'revol_util': [revol_util],
            'annual_inc': [annual_inc],
            'avg_cur_bal': [avg_cur_bal],
            'total_acc': [total_acc],
            'acc_open_past_24mths': [acc_open_past_24mths],
            'total_bc_limit': [total_bc_limit],
            'total_il_high_credit_limit': [total_il_high_credit_limit],
            'total_rev_hi_lim': [total_rev_hi_lim],
            'emp_length': [emp_length],
            'total_bal_ex_mort': [total_bal_ex_mort],
            'bc_open_to_buy': [bc_open_to_buy]
        })
        
        cat_boost_clf=CatBoostClassifier()
        cat_boost_clf.load_model("fiz_litza_model.cbm")
        res = cat_boost_clf.predict(df)[0]
        print(res)
        return res
    except Exception:
        return False
    