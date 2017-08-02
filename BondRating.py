from WindPy import w
from datetime import *
w.start()

import numpy as np


class BondRating():
    def _init_(self):
        pass

    def PastData(self, s_info_code):
        #######企业背景
        background = w.wsd(s_info_code, "holder_pct,nature,net_profit_is,np_belongto_parcomsh",
                           "2005-12-30", "2016-12-31", "order=1;unit=1;rptType=1;Period=Y;Days=Alldays")

        self.rpt_period = background.Times
        FullLength = np.size(self.rpt_period)

        # 企业性质，大股东比例，净利润，归母净利润
        self.nature = background.Data[0]
        self.holder_pct = background.Data[1]
        self.net_profit_is = np.array(background.Data[2]) / 10000 / 10000
        self.np_belong_to_parcomsh = np.array(background.Data[3]) / 10000 / 10000

        # 母公司利润占比 = 归母净利润/净利润(当净利润为正)，打分为-0.5（当净利润为负）





        ######规模指标
        # 总资产规模
        scale = w.wsd(s_info_code, "tot_assets,tot_equity,tot_oper_rev,opprofit",
                      "2005-12-30", "2016-12-31", "unit=1;rptType=1;Period=Y;Days=Alldays")
        # 资产总计
        self.tot_assets = np.array(scale.Data[0]) / 10000 / 10000
        # 所有者权益合计
        self.tot_equity = np.array(scale.Data[1]) / 10000 / 10000
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
        ebitda = fin_exp_is + tot_profit + depr_fa_coga_dpba + amort_intang_assets + amort_lt_deferred_exp + decr_deferred_exp + incr_acc_exp + loss_disp_fiolta + loss_fv_chg

        # 经营现金流净额
        net_cash_flows_oper_act = np.array(w.wsd(s_info_code, "net_cash_flows_oper_act",
                                                 "2005-12-30", "2017-01-01", "unit=1;rptType=1;Period=Y").Data[
                                               0]) / 10000 / 10000

        ######盈利指标
        # 毛利率
        # 营业成本，营业税费，营业收入
        oper_cost, taxes_surcharges_ops, oper_rev = np.array(
            w.wsd(s_info_code, "oper_cost,taxes_surcharges_ops,oper_rev", "2005-12-30", "2016-12-31",
                  "unit=1;rptType=1;Period=Y;Days=Alldays").Data)
        # 毛利率
        self.gross_profit_margin = (1 - (oper_cost + taxes_surcharges_ops) / oper_rev) * 100

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
        monetary_cap, wgsd_invest_trading, notes_rcv, acct_rcv, non_cur_assets_due_within_1y = w.wsd("136164.SH",
                                                                                                     "monetary_cap,wgsd_invest_trading,notes_rcv,acct_rcv,non_cur_assets_due_within_1y",
                                                                                                     "2005-12-30",
                                                                                                     "2016-12-31",
                                                                                                     "unit=1;rptType=1;currencyType=;Period=Y;Days=Alldays")
        return self