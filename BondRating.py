from WindPy import w
from datetime import *
w.start()

import numpy as np

from nan_to_0 import *
from RateFun import *
from RateFunInverse import *


class BondRating():
    def _init_(self):
        pass

    def PastData(self, s_info_code):
        #######企业背景
        background = w.wsd(s_info_code, "holder_pct,net_profit_is,np_belongto_parcomsh",
                           "2005-12-30", "2016-12-31", "order=1;unit=1;rptType=1;Period=Y;Days=Alldays")

        self.rpt_period = background.Times
        FullLength = np.size(self.rpt_period)
        self.FullLength = FullLength

        # 企业性质，大股东比例，净利润，归母净利润
        self.holder_pct = np.array(background.Data[0])
        self.net_profit_is = np.array(background.Data[1]) / 10000 / 10000
        self.np_belong_to_parcomsh = np.array(background.Data[2]) / 10000 / 10000

        # 母公司利润占比 = 归母净利润/净利润(当净利润为正)，打分为-0.5（当净利润为负）
        self.np_belong_to_parcomsh_ratio = self.np_belong_to_parcomsh/self.net_profit_is


        ######规模指标
        # 总资产规模
        scale = w.wsd(s_info_code, "tot_assets,tot_equity,tot_oper_rev,opprofit",
                      "2005-12-30", "2016-12-31", "unit=1;rptType=1;Period=Y;Days=Alldays")
        # 资产总计#总资产规模
        self.tot_assets = np.array(scale.Data[0]) / 10000 / 10000
        # 所有者权益合计#净资产合计
        self.tot_equity = np.array(scale.Data[1]) / 10000 / 10000
        # 净资产变化率########
        self.pct_chg_tot_equity = ((self.tot_equity[1:FullLength] - self.tot_equity[0:FullLength-1])/self.tot_equity[0:FullLength-1])[1:FullLength-1]


        # 营业总收入
        self.tot_oper_rev = np.array(scale.Data[2]) / 10000 / 10000
        # 净利润在前面
        # 营业利润
        self.opprofit = np.array(scale.Data[3]) / 10000 / 10000

        # EBITDA
        ebitda_pre = w.wsd(s_info_code,
                           "fin_exp_is,tot_profit,depr_fa_coga_dpba,amort_intang_assets,amort_lt_deferred_exp,decr_deferred_exp,incr_acc_exp,loss_disp_fiolta,loss_scr_fa,loss_fv_chg",
                           "2005-12-30", "2016-12-31", "unit=1;rptType=1;Period=Y;Days=Alldays")
        # 财务费用
        fin_exp_is = np.array(ebitda_pre.Data[0]) / 10000 / 10000
        # 利润总额
        tot_profit = np.array(ebitda_pre.Data[1]) / 10000 / 10000
        # 固定资产折旧、油气资产折耗、生产性生物资产折旧
        depr_fa_coga_dpba = np.array(ebitda_pre.Data[2]) / 10000 / 10000
        # 无形资产摊销
        amort_intang_assets = np.array(ebitda_pre.Data[3]) / 10000 / 10000
        # 长期待摊费用摊销
        amort_lt_deferred_exp = np.array(ebitda_pre.Data[4]) / 10000 / 10000
        # 待摊费用减少
        decr_deferred_exp = np.array(ebitda_pre.Data[5]) / 10000 / 10000
        where_are_nan = np.isnan(decr_deferred_exp)
        decr_deferred_exp[where_are_nan] = 0
        # 预提费用增加
        incr_acc_exp = np.array(ebitda_pre.Data[6]) / 10000 / 10000
        where_are_nan = np.isnan(incr_acc_exp)
        incr_acc_exp[where_are_nan] = 0
        # 处置固定资产、无形资产和其他长期资产的损失
        loss_disp_fiolta = np.array(ebitda_pre.Data[7]) / 10000 / 10000
        # 固定资产报废损失
        ##为空
        loss_scr_fa = np.array(ebitda_pre.Data[8]) / 10000 / 10000
        where_are_nan = np.isnan(loss_scr_fa)
        loss_scr_fa[where_are_nan] = 0
        # 公允价值变动损失
        ##为空
        loss_fv_chg = np.array(ebitda_pre.Data[9]) / 10000 / 10000
        where_are_nan = np.isnan(loss_fv_chg)
        loss_fv_chg[where_are_nan] = 0

        # EBITDA = 利润总额 + 费用化利息支出 + 固定资产折旧 + 摊销
        self.ebitda = fin_exp_is + tot_profit + depr_fa_coga_dpba + amort_intang_assets + amort_lt_deferred_exp + decr_deferred_exp + incr_acc_exp + loss_disp_fiolta + loss_fv_chg

        # 经营现金流净额
        self.net_cash_flows_oper_act = np.array(w.wsd(s_info_code, "net_cash_flows_oper_act",
                                                 "2005-12-30", "2017-01-01", "unit=1;rptType=1;Period=Y").Data[
                                               0]) / 10000 / 10000

        ######盈利指标
        # 毛利率
        # 营业成本，营业税费，营业收入
        oper_cost, taxes_surcharges_ops, oper_rev = np.array(
            w.wsd(s_info_code, "oper_cost,taxes_surcharges_ops,oper_rev", "2005-12-30", "2016-12-31",
                  "unit=1;rptType=1;Period=Y;Days=Alldays").Data)/10000/10000
        # 毛利率
        self.gross_profit_margin = (1 - (oper_cost + taxes_surcharges_ops) / oper_rev)

        # 净利率 = 净利润/营业收入
        self.net_profit_margin = self.net_profit_is / oper_rev

        # 3年毛利率标准差
        # 此处使用std(今年、去年、前年主营业务收入)/avg(今年、去年、前年主营业务收入)
        # 从2007-->2016年值
        self.std_gross_profit_margin = np.zeros(FullLength - 2)
        for i in range(0, FullLength - 2):
            self.std_gross_profit_margin[i] = np.std(oper_rev[i:i + 3], ddof=1) / np.mean(oper_rev[i:i + 3])

        # 毛利率变化值 = 今年毛利率 - 去年毛利率
        # 从2007-->2016年值
        self.chg_gross_profit_margin = (self.gross_profit_margin[1:FullLength] - self.gross_profit_margin[
                                                                                 0:FullLength - 1])[1:FullLength - 1]

        # ROE
        self.ROE = np.array(w.wsd(s_info_code, "roe", "2005-12-30", "2016-12-31", "Period=Y;Days=Alldays").Data[0])


        #####债务情况
        # (现金 - 短债)/净资产 -- (含应收应付)
        # (货币性资产 - 短期债务)/净资产
        # 货币性资产 = 货币资金 + 交易性金融资产 + 应收票据 + 应收账款 + 一年内到期的非流动资产---资产负债表
        # 注：交易性金融资产数据来源于全球资产负债表，其余来自中国资产负债表
        # 货币资金, 交易性金融资产, 应收票据, 应收账款, 一年内到期的非流动资产
        monetary_cap, tradable_fin_assets, notes_rcv, acct_rcv, non_cur_assets_due_within_1y = nan_to_0(np.array(w.wsd(
            s_info_code, "monetary_cap,tradable_fin_assets,notes_rcv,acct_rcv,non_cur_assets_due_within_1y", "2005-12-31", "2016-12-31",
            "unit=1;rptType=1;Period=Y;Days=Alldays").Data))/10000/10000
        #货币型资产，含应付应收
        monetary_asset_rcv = monetary_cap + tradable_fin_assets + notes_rcv + acct_rcv + non_cur_assets_due_within_1y

        #短期债务 = 短期借款+向中央银行借款+交易行金融负债+应付票据+应付账款+应付手续费及佣金+应付职工薪酬+应交税费+应付利息+其他应付款+一年内到期的非流动负债
        st_borrow, borrow_central_bank, tradable_fin_liab, notes_payable, acct_payable, handling_charges_comm_payable, \
        empl_ben_payable, taxes_surcharges_payable, int_payable, oth_payable, non_cur_liab_due_within_1y \
            = nan_to_0(np.array(w.wsd(s_info_code, "st_borrow,borrow_central_bank,tradable_fin_liab,notes_payable,acct_payable,handling_charges_comm_payable,\
            empl_ben_payable,taxes_surcharges_payable,int_payable,oth_payable,non_cur_liab_due_within_1y",
                                      "2005-12-31", "2016-12-31",
                                      "unit=1;rptType=1;Period=Y;Days=Alldays").Data) / 10000 / 10000)
        #短期债务
        short_term_debt_payable = st_borrow + borrow_central_bank + tradable_fin_liab + notes_payable + acct_payable + handling_charges_comm_payable + \
                                  empl_ben_payable + taxes_surcharges_payable + int_payable + oth_payable + non_cur_liab_due_within_1y

        #(现金 - 短债)/净资产 -- (含应收应付)
        self.cash_debt_div_assets_1 = (monetary_asset_rcv - short_term_debt_payable)/self.tot_equity

        #(现金 - 短债)/净资产 -- (有息债务)
        monetary_asset_2 = monetary_cap + tradable_fin_assets + non_cur_assets_due_within_1y
        short_term_debt_2 = st_borrow + borrow_central_bank + non_cur_liab_due_within_1y
        self.cash_debt_div_assets_2 = (monetary_asset_2 - short_term_debt_2)/self.tot_assets

        #有息负债率 =  （短期借款+向中央银行借款+一年内到期的非流动负债+长期借款+应付债券）/资产总计
        # = （short_term_debt_2 + 长期借款 + 应付债券）/self.tot_assets
        #长期借款，应付债券
        lt_borrow, bonds_payable = np.array(w.wsd(s_info_code, "lt_borrow,bonds_payable", "2005-12-30", "2016-12-31", "unit=1;rptType=1;Period=Y;Days=Alldays").Data)/10000/10000
        self.liab_with_interest_ratio = (short_term_debt_2 + lt_borrow + bonds_payable)/self.tot_assets

        #有息负债率变化值(%)#2007--->2016
        self.chg_liab_with_interest_ratio = (self.liab_with_interest_ratio[1:FullLength] - self.liab_with_interest_ratio[0:FullLength-1])[1:FullLength-1]

        #资产负债率 = 负债合计/负债和所有者权益总计
        tot_liab, tot_liab_shrhldr_eqy = np.array(w.wsd(s_info_code, "tot_liab,tot_liab_shrhldr_eqy", "2015-12-30", "2016-12-31",
                                                        "unit=1;rptType=1;Period=Y;Days=Alldays").Data)/10000/10000
        #资产负债率（%）
        self.debt_to_asset_ratio = tot_liab/tot_liab_shrhldr_eqy

        #三费费率 = （销售费用+管理费用+财务费用）/营业收入(oper_rev)
        selling_dist_exp, gerl_admin_exp, fin_exp_is = np.array(w.wsd(s_info_code, "selling_dist_exp,gerl_admin_exp,fin_exp_is", "2005-12-30", "2016-12-31", "unit=1;rptType=1;Period=Y;Days=Alldays").Data)/10000/10000
        self.three_exp_ratio = (selling_dist_exp + gerl_admin_exp + fin_exp_is)/oper_rev


      #运营效率
        #固定资产/总资产
        #=（长期股权投资 + 投资性房地产 + 固定资产 + 在建工程 + 工程物资 + 固定资产清理 + 生产性生物物资 + 油气资产 + 无形资产 + 其他非流动资产
        long_term_eqy_invest, invest_real_estate, fix_assets, const_in_prog, proj_matl, fix_assets_disp, \
        productive_bio_assets, oil_and_natural_gas_assets, intang_assets, oth_non_cur_assets = \
            nan_to_0(np.array(w.wsd(s_info_code, "long_term_eqy_invest,invest_real_estate,fix_assets,const_in_prog,proj_matl,\
            fix_assets_disp,productive_bio_assets,oil_and_natural_gas_assets,intang_assets,oth_non_cur_assets",
                           "2005-12-30", "2016-12-31", "unit=1;rptType=1;Period=Y;Days=Alldays").Data))/10000/10000
        #固定资产/总资产（%）
        self.fix_assets_ratio = (long_term_eqy_invest + invest_real_estate + fix_assets + const_in_prog + proj_matl + fix_assets_disp +
            productive_bio_assets + oil_and_natural_gas_assets + intang_assets + oth_non_cur_assets)/self.tot_assets


        #经营现金流/总债务 = 经营活动产生的现金流量净额/（短期债务（含应付应收short_term_debt_payable）+长期借款+应付债券+长期应付款+专项应付款）
        #长期借款，应付债券：lt_borrow, bonds_payable
        #长期应付款，专项应付款
        lt_payable, specific_item_payable = nan_to_0(np.array(w.wsd(s_info_code,"lt_payable,specific_item_payable", "2005-12-30", "2016-12-31",
                  "unit=1;rptType=1;Period=Y;Days=Alldays").Data))/10000/10000
        tot_debt = short_term_debt_payable + lt_borrow + bonds_payable + lt_payable + specific_item_payable

        #经营现金流/总债务(%)
        self.cash_flows_oper_debt_ratio = self.net_cash_flows_oper_act/tot_debt

        #三年经营现金流波动(%)
        #2007-->2016
        self.std_cash_flows_oper = np.zeros(FullLength - 2)
        for i in range(0, FullLength - 2):
            self.std_cash_flows_oper[i] = np.std(self.net_cash_flows_oper_act[i:i+3], ddof=1)/np.mean(self.net_cash_flows_oper_act[i:i+3])


        #EBITDA/总债务
        self.ebitda_debt_ratio = self.ebitda/tot_debt

        #固定资产周转率，存货周转天数
        self.faturn, self.invturndays = np.array(w.wsd(s_info_code, "faturn, invturndays", "2005-12-30", "2016-12-31", "Period=Y;Days=Alldays").Data)


        #应收账款周转天数 = 360/应收账款周转率
        #应收账款周转率 = 营业收入/（去年、今年平均（应收账款+其他应收款+长期应收款））
        #营业收入 oper_rev
        #应收账款 acct_rcv
        #其他应收款，长期应收款
        oth_rcv, long_term_rec = nan_to_0(np.array(w.wsd(s_info_code, "oth_rcv,long_term_rec", "2005-12-30", "2016-12-31", "unit=1;rptType=1;Period=Y;Days=Alldays").Data))/10000/10000

        #应收账款周转天数
        self.acc_rev_turndays = 360 / (oper_rev[2:FullLength] / (
        (acct_rcv[1:FullLength - 1] + acct_rcv[2:FullLength] + oth_rcv[1:FullLength - 1] + oth_rcv[2:FullLength]
         + long_term_rec[1:FullLength - 1] + long_term_rec[2:FullLength]) / 2))


        #####增信手段
        #未使用授信/总债务
        #未使用银行授信额度
        credit_lineunused = nan_to_0(np.array(w.wsd("136164.SH", "credit_lineunused", "2005-12-30", "2016-12-31",
                                                    "Period=Y;Days=Alldays").Data[0]))
        self.credit_unused_debt_ratio = credit_lineunused/tot_debt*100


        return self


    def score(self, Table1):

        ScoringCriterion = np.array(Table1)
        ####企业背景
        self.holder_pct_score = RateFun(self.holder_pct, ScoringCriterion[0])
        #母公司利润占比，当净利润为负时，打分为-0.5
        self.np_belong_to_parcomsh_ratio_score = RateFun(self.np_belong_to_parcomsh_ratio, ScoringCriterion[1])
        self.np_belong_to_parcomsh_ratio_score[self.net_profit_is < 0] = -0.5


        ####规模指标
        self.tot_assets_score = RateFun(self.tot_assets, ScoringCriterion[2])
        self.tot_equity_score = RateFun(self.tot_equity, ScoringCriterion[3])
        self.pct_chg_tot_equity_score = RateFun(self.pct_chg_tot_equity, ScoringCriterion[4])
        self.tot_oper_rev_score = RateFun(self.tot_oper_rev, ScoringCriterion[5])
        self.net_profit_margin_score = RateFun(self.net_profit_margin, ScoringCriterion[6])
        self.opprofit_score = RateFun(self.opprofit, ScoringCriterion[7])
        self.ebitda_score = RateFun(self.opprofit, ScoringCriterion[8])
        self.net_cash_flows_oper_act_score = RateFun(self.net_cash_flows_oper_act, ScoringCriterion[9])

        ####盈利指标
        self.gross_profit_margin_score = RateFun(self.gross_profit_margin, ScoringCriterion[10])
        self.net_profit_margin_score = RateFun(self.net_profit_margin, ScoringCriterion[11])
        ######三年毛利率标准差，改，越低分数越高
        self.std_gross_profit_margin_score = RateFunInverse(self.std_gross_profit_margin, ScoringCriterion[12])
        self.chg_gross_profit_margin_score = RateFun(self.chg_gross_profit_margin, ScoringCriterion[13])
        self.ROE_score = RateFun(self.ROE, ScoringCriterion[14])

        ####债务情况
        self.cash_debt_div_assets_1_score = RateFun(self.cash_debt_div_assets_1, ScoringCriterion[15])
        self.cash_debt_div_assets_2_score = RateFun(self.cash_debt_div_assets_2, ScoringCriterion[16])
        ###有息负债率、有息负债率变化值、资产负债率、三费费率改
        self.liab_with_interest_ratio_score = RateFunInverse(self.liab_with_interest_ratio, ScoringCriterion[17])
        ##
        self.chg_liab_with_interest_ratio_score = RateFunInverse(self.chg_liab_with_interest_ratio, ScoringCriterion[18])
        ##
        self.debt_to_asset_ratio_score = RateFunInverse(self.debt_to_asset_ratio, ScoringCriterion[19])
        ##
        self.three_exp_ratio_score = RateFunInverse(self.three_exp_ratio, ScoringCriterion[20])

        ####运营效率
        self.fix_assets_ratio_score = RateFun(self.fix_assets_ratio, ScoringCriterion[21])
        self.cash_flows_oper_debt_ratio_score = RateFun(self.cash_flows_oper_debt_ratio, ScoringCriterion[22])
        ##三年经营现金流波动，改
        self.std_cash_flows_oper_score = RateFunInverse(self.std_cash_flows_oper, ScoringCriterion[23])
        self.ebitda_debt_ratio_score = RateFun(self.ebitda_debt_ratio, ScoringCriterion[24])
        self.faturn_score = RateFun(self.faturn, ScoringCriterion[25])
        #存货周转天数，改
        self.invturndays_score = RateFunInverse(self.invturndays, ScoringCriterion[26])
        #应收账款周转天数，改
        self.acc_rev_turndays_score = RateFunInverse(self.acc_rev_turndays, ScoringCriterion[27])

        self.ScoreTable = np.vstack((self.holder_pct_score[2:self.FullLength], self.np_belong_to_parcomsh_ratio_score[2:self.FullLength],
                                     self.tot_equity_score[2:self.FullLength]))





        return self.ScoreTable


    # def Rate(self, weight, other_score):
    #     RateScore = self.holder_pct_score*0.015 + self.np_belong_to_parcomsh_ratio_score*0.02 + self.tot_assets_score*0.08 +\
    #                 self.tot_equity_score*0.075 + self.pct_chg_tot_equity_score*0.005 + self.tot_oper_rev_score*0.05 + \
    #                 self.net_profit_is * 0.015 + self.opprofit_score*0.015 + self.ebitda_score*0.05 + self.net_cash_flows_oper_act_score*0.005+\
    #                 self.gross_profit_margin_score * 0.01 + self.net_profit_margin_score*0.03 + self.std_gross_profit_margin_score*0.005 +\
    #                 self.chg_gross_profit_margin_score * 0.005 + self.ROE_score*0.015











