from WindPy import w
from datetime import *
w.start()

import numpy as np
import pandas as pd
from RateFunNew import *
from RateFunSpecial import *
from Score2Rate import *

#PastData: Get the data from Wind online API data. Return df_temp
#score: Get the score according to the criterion and the df_temp. Return df_score
#rate: Get the final rate for the bond. Return df_rate
class BondRatingNew():
    def __init__(self):
        pass

    def PastData(self, s_info_code):
        background = w.wsd(s_info_code, "holder_pct,net_profit_is,np_belongto_parcomsh,tot_assets,tot_equity,tot_oper_rev,opprofit, \
        fin_exp_is,tot_profit,depr_fa_coga_dpba,amort_intang_assets,amort_lt_deferred_exp,decr_deferred_exp, \
        incr_acc_exp,loss_disp_fiolta,loss_scr_fa,loss_fv_chg, net_cash_flows_oper_act,oper_cost,taxes_surcharges_ops,oper_rev,roe,\
        monetary_cap,tradable_fin_assets,notes_rcv,acct_rcv,non_cur_assets_due_within_1y,st_borrow,borrow_central_bank,\
        tradable_fin_liab,notes_payable,acct_payable,handling_charges_comm_payable, \
        empl_ben_payable,taxes_surcharges_payable,int_payable,oth_payable,non_cur_liab_due_within_1y,lt_borrow,bonds_payable, \
        tot_liab,tot_liab_shrhldr_eqy,selling_dist_exp,gerl_admin_exp,long_term_eqy_invest,invest_real_estate, \
        fix_assets,const_in_prog,proj_matl,fix_assets_disp,productive_bio_assets,oil_and_natural_gas_assets,intang_assets, \
        oth_non_cur_assets,lt_payable,specific_item_payable,faturn, invturndays,oth_rcv,long_term_rec",
                           "2007-12-30", "2016-12-31", "order=1;unit=1;rptType=1;Period=Y;Days=Alldays")

        data = background.Data
        index = background.Fields
        columns = range(background.Times[0].year, background.Times[len(background.Times) - 1].year + 1)
        df_RawData = pd.DataFrame(data=data, index=index, columns=columns)
        #get column numbers
        col_num = df_RawData.shape[1]

        #process NaN
        df_RawData = df_RawData.replace('Nan',0)
        unit = 1e8

        #build a new DF df_temp--data to score,
        #datetime: column[2:]
        df_temp = pd.DataFrame(columns=columns[2:])
        df_temp.ix["大股东比例"] = df_RawData.ix["HOLDER_PCT"][2:] / 100
        df_temp.ix["母公司利润占比"] = df_RawData.ix["NP_BELONGTO_PARCOMSH"] / df_RawData.ix["NET_PROFIT_IS"][2:]
        df_temp.ix["总资产规模"] = df_RawData.ix["TOT_ASSETS"][2:] / unit
        df_temp.ix["净资产规模"] = df_RawData.ix["TOT_EQUITY"][2:] / unit

        df_temp.ix["净资产变化率"] = np.empty(col_num - 2)
        for i in range(0, col_num - 2):
            if df_RawData.ix["TOT_EQUITY"].iloc[i+1] == 0:
                df_temp.ix["净资产变化率"].iloc[i] = 'NaN'
            else:
                df_temp.ix["净资产变化率"].iloc[i] = (df_RawData.ix["TOT_EQUITY"].iloc[i+2] - df_RawData.ix["TOT_EQUITY"].iloc[i+1]
                                                )/df_RawData.ix["TOT_EQUITY"].iloc[i+1]

        # 正在改
        # df_temp.ix["净资产变化率"] = (np.array(df_RawData.ix["TOT_EQUITY"][2:]) - np.array(df_RawData.ix["TOT_EQUITY"][1:col_num - 1]))/ \
        #                        np.array(df_RawData.ix["TOT_EQUITY"][1:col_num - 1])


        df_temp.ix["营业收入"] = df_RawData.ix["TOT_OPER_REV"][2:] / unit
        df_temp.ix["净利润"] = df_RawData.ix["NET_PROFIT_IS"][2:] / unit
        df_temp.ix["营业利润"] = df_RawData.ix["OPPROFIT"][2:] / unit
        # Attention: str--->float
        df_temp.ix["EBITDA"] = (df_RawData.ix["FIN_EXP_IS"] + df_RawData.ix["TOT_PROFIT"] + df_RawData.ix["DEPR_FA_COGA_DPBA"] + \
            df_RawData.ix["AMORT_INTANG_ASSETS"] + df_RawData.ix["AMORT_LT_DEFERRED_EXP"] + df_RawData.ix["DECR_DEFERRED_EXP"] + \
            df_RawData.ix["INCR_ACC_EXP"] + df_RawData.ix["LOSS_DISP_FIOLTA"] + df_RawData.ix["LOSS_FV_CHG"])[2:]/unit

        df_temp.ix["经营现金流净额"] = df_RawData.ix["NET_CASH_FLOWS_OPER_ACT"][2:] / unit

        # 盈利指标
        df_temp.ix["毛利率"] = (1 - (df_RawData.ix["OPER_COST"] + df_RawData.ix["TAXES_SURCHARGES_OPS"]) / df_RawData.ix["OPER_REV"])[2:]
        df_temp.ix["净利率"] = (df_RawData.ix["NET_PROFIT_IS"]/df_RawData.ix["OPER_REV"])[2:]

        df_temp.ix["过去三年毛利率标准差"] = np.empty(col_num - 2)
        for i in range(0, col_num - 2):
            if df_RawData.ix["OPER_REV"].iloc[i + 2] == 0:
                df_temp.ix["过去三年毛利率标准差"].iloc[i] = 'NaN'
            else:
                df_temp.ix["过去三年毛利率标准差"].iloc[i] = np.std(df_RawData.ix["OPER_REV"].iloc[i:i + 3], ddof=1) / np.mean(
                    df_RawData.ix["OPER_REV"].iloc[i:i + 3])

        df_temp.ix["毛利率变化值"] = np.array(df_temp.ix["毛利率"]) - np.array(1 - (df_RawData.ix["OPER_COST"] + df_RawData.ix["TAXES_SURCHARGES_OPS"]) / df_RawData.ix["OPER_REV"])[1:col_num-1]
        df_temp.ix["ROE"] = df_RawData.ix["ROE"][2:]/100

        df_temp.ix["(现金-短债)/净资产, 含应付应收"] = (((df_RawData.ix["MONETARY_CAP"] + df_RawData.ix["TRADABLE_FIN_ASSETS"]
        + df_RawData.ix["NOTES_RCV"] + df_RawData.ix["ACCT_RCV"] + df_RawData.ix["NON_CUR_ASSETS_DUE_WITHIN_1Y"])
        - (df_RawData.ix["ST_BORROW"] + df_RawData.ix["BORROW_CENTRAL_BANK"] + df_RawData.ix["TRADABLE_FIN_LIAB"]
           + df_RawData.ix["NOTES_PAYABLE"] + df_RawData.ix["ACCT_PAYABLE"] + df_RawData.ix["HANDLING_CHARGES_COMM_PAYABLE"]
           + df_RawData.ix["EMPL_BEN_PAYABLE"] + df_RawData.ix["TAXES_SURCHARGES_PAYABLE"] + df_RawData.ix["INT_PAYABLE"]
           + df_RawData.ix["OTH_PAYABLE"] + df_RawData.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"]))/df_RawData.ix["TOT_EQUITY"])[2:]

        df_temp.ix["(现金-短债)/净资产，含有息债务"] = (((df_RawData.ix["MONETARY_CAP"] + df_RawData.ix["TRADABLE_FIN_ASSETS"]
                                            + df_RawData.ix["NON_CUR_ASSETS_DUE_WITHIN_1Y"])
                                           - (df_RawData.ix["ST_BORROW"] + df_RawData.ix["BORROW_CENTRAL_BANK"]
                                              +df_RawData.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"]))/df_RawData.ix["TOT_EQUITY"])[2:]

        df_temp.ix["有息负债率"] = ((df_RawData.ix["ST_BORROW"] + df_RawData.ix["BORROW_CENTRAL_BANK"]
                               + df_RawData.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + df_RawData.ix["LT_BORROW"] + df_RawData.ix["BONDS_PAYABLE"])/df_RawData.ix["TOT_ASSETS"])[2:]

        df_temp.ix["有息负债变化值"] = np.array((df_RawData.ix["ST_BORROW"] + df_RawData.ix["BORROW_CENTRAL_BANK"] +
                                           df_RawData.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + df_RawData.ix["LT_BORROW"] +
                                           df_RawData.ix["BONDS_PAYABLE"]) / df_RawData.ix["TOT_ASSETS"])[
                                 2:] - np.array((df_RawData.ix["ST_BORROW"] + df_RawData.ix["BORROW_CENTRAL_BANK"] +
                                                 df_RawData.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + df_RawData.ix[
                                                     "LT_BORROW"] + df_RawData.ix["BONDS_PAYABLE"]) / df_RawData.ix[
                                                    "TOT_ASSETS"])[1:col_num - 1]

        df_temp.ix["资产负债率"] = df_RawData.ix["TOT_LIAB"] / df_RawData.ix["TOT_LIAB_SHRHLDR_EQY"][2:]
        df_temp.ix["三费费率"] = (df_RawData.ix["SELLING_DIST_EXP"] + df_RawData.ix["GERL_ADMIN_EXP"] + df_RawData.ix["FIN_EXP_IS"]) / df_RawData.ix["OPER_REV"][2:]

        df_temp.ix["固定资产/总资产"] = (df_RawData.ix["LONG_TERM_EQY_INVEST"] + df_RawData.ix["INVEST_REAL_ESTATE"] + df_RawData.ix["FIX_ASSETS"]
                                  + df_RawData.ix["CONST_IN_PROG"] + df_RawData.ix["PROJ_MATL"] + df_RawData.ix["FIX_ASSETS_DISP"]
                                  + df_RawData.ix["PRODUCTIVE_BIO_ASSETS"] + df_RawData.ix["OIL_AND_NATURAL_GAS_ASSETS"] + df_RawData.ix["INTANG_ASSETS"]
                                  + df_RawData.ix["OTH_NON_CUR_ASSETS"])/df_RawData.ix["TOT_ASSETS"][2:]

        df_temp.ix["经营现金流/总债务"] = (df_RawData.ix["NET_CASH_FLOWS_OPER_ACT"]/(df_RawData.ix["ST_BORROW"] + df_RawData.ix["BORROW_CENTRAL_BANK"] + df_RawData.ix["TRADABLE_FIN_LIAB"]\
                                  + df_RawData.ix["NOTES_PAYABLE"] + df_RawData.ix["ACCT_PAYABLE"] + df_RawData.ix["HANDLING_CHARGES_COMM_PAYABLE"]\
                                  + df_RawData.ix["EMPL_BEN_PAYABLE"] + df_RawData.ix["TAXES_SURCHARGES_PAYABLE"] + df_RawData.ix["INT_PAYABLE"]\
                                  + df_RawData.ix["OTH_PAYABLE"] + df_RawData.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + df_RawData.ix["LT_BORROW"] \
                                   + df_RawData.ix["BONDS_PAYABLE"] + df_RawData.ix["LT_PAYABLE"] + df_RawData.ix["SPECIFIC_ITEM_PAYABLE"]))[2:]

        df_temp.ix["三年经营现金流波动"] = np.empty(col_num - 2)
        for i in range(0, col_num - 2):
            if df_RawData.ix["NET_CASH_FLOWS_OPER_ACT"].iloc[i + 2] == 0:
                df_temp.ix["三年经营现金流波动"].iloc[i] = 'NaN'
            else:
                df_temp.ix["三年经营现金流波动"].iloc[i] = np.std(df_RawData.ix["NET_CASH_FLOWS_OPER_ACT"].iloc[i: i + 3],
                                                         ddof=1) / np.mean(
                    df_RawData.ix["NET_CASH_FLOWS_OPER_ACT"].iloc[i:i + 3])

        df_temp.ix["EBITDA/总债务"] = (df_temp.ix["EBITDA"]/((df_RawData.ix["ST_BORROW"] + df_RawData.ix["BORROW_CENTRAL_BANK"] + df_RawData.ix["TRADABLE_FIN_LIAB"]\
                                  + df_RawData.ix["NOTES_PAYABLE"] + df_RawData.ix["ACCT_PAYABLE"] + df_RawData.ix["HANDLING_CHARGES_COMM_PAYABLE"]\
                                  + df_RawData.ix["EMPL_BEN_PAYABLE"] + df_RawData.ix["TAXES_SURCHARGES_PAYABLE"] + df_RawData.ix["INT_PAYABLE"]\
                                  + df_RawData.ix["OTH_PAYABLE"] + df_RawData.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + df_RawData.ix["LT_BORROW"] \
                                   + df_RawData.ix["BONDS_PAYABLE"] + df_RawData.ix["LT_PAYABLE"] + df_RawData.ix["SPECIFIC_ITEM_PAYABLE"])/unit))[2:]

        df_temp.ix["固定资产周转率"] = df_RawData.ix["FATURN"][2:]
        df_temp.ix["存货周转天数"] = df_RawData.ix["INVTURNDAYS"][2:]
        df_temp.ix["应收账款周转天数"] = 360 / (df_RawData.ix["OPER_REV"][2:] / ((np.array(
            df_RawData.ix["ACCT_RCV"][1:col_num - 1] + df_RawData.ix["OTH_RCV"][1:col_num - 1] + df_RawData.ix[
                                                                                                     "LONG_TERM_REC"][
                                                                                                 1:col_num - 1]) + np.array(
            df_RawData.ix["ACCT_RCV"][2:] + df_RawData.ix["OTH_RCV"][2:] + df_RawData.ix["LONG_TERM_REC"][2:])) / 2))

        #####除2013， 2014年外不同
        df_temp.ix["未使用授信/总债务"] = w.wss(s_info_code, "credit_lineunused").Data[0][0]/\
                                  ((df_RawData.ix["ST_BORROW"] + df_RawData.ix["BORROW_CENTRAL_BANK"] +
                                    df_RawData.ix["TRADABLE_FIN_LIAB"] + df_RawData.ix["NOTES_PAYABLE"] +
                                    df_RawData.ix["ACCT_PAYABLE"] + df_RawData.ix["HANDLING_CHARGES_COMM_PAYABLE"]
                                    + df_RawData.ix["EMPL_BEN_PAYABLE"] + df_RawData.ix["TAXES_SURCHARGES_PAYABLE"]
                                    + df_RawData.ix["INT_PAYABLE"] + df_RawData.ix["OTH_PAYABLE"]
                                    + df_RawData.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + df_RawData.ix["LT_BORROW"]
                                    + df_RawData.ix["BONDS_PAYABLE"] + df_RawData.ix["LT_PAYABLE"] +
                                    df_RawData.ix["SPECIFIC_ITEM_PAYABLE"])/unit)[2:]


        self.df_temp = df_temp

        return self

    def score(self, ScoringCriterion, OtherScore):
        index = self.df_temp.index
        df_score = pd.DataFrame(columns=self.df_temp.columns, index = index)
        for i in range(0, index.size):
            df_score.ix[index[i]] = RateFunNew(self.df_temp.ix[index[i]], ScoringCriterion.ix[index[i]])
        #merge df_score and OtherScore
        df_score = pd.concat([df_score, OtherScore])

        self.df_score = df_score
        return self

    def rate(self, weight):
        df_rate = pd.DataFrame(columns = self.df_score.columns)
        self.df_score = self.df_score.reindex(weight.index)
        df_rate.ix["内部得分-债项"] = np.dot(weight.T, self.df_score)[0]
        df_rate.ix["内部评级-债项"] = Score2Rate(df_rate.ix["内部得分-债项"])
        weight_body = weight.drop(["外部担保", "资产抵押担保"], axis = 0)
        df_score_body = self.df_score.drop(["外部担保", "资产抵押担保"], axis = 0)
        df_rate.ix["内部得分-主体"] = np.dot(weight_body.T, df_score_body)[0]
        df_rate.ix["内部评级-主体"] = Score2Rate(df_rate.ix["内部得分-主体"])




        return df_rate







