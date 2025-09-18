from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from credit.models import UrClient



fromNumbToAcra=["Неизвестно","AAA(ru)","AA+(ru)","AA(ru)","AA-(ru)","A+(ru)","A(ru)","A-(ru)","BBB+(ru)","BBB(ru)","BBB-(ru)","BB+(ru)","BB(ru)","BB-(ru)","B+(ru)","B(ru)","B-(ru)","CCC(ru)","CC(ru)","C(ru)","SD(ru)","D(ru)"]
fromNumbToExpert=["Неизвестно","ruAAA","ruAA+","ruAA","ruAA-","ruA+","ruA","ruA-","ruBBB+","ruBBB","ruBBB-","ruBB+","ruBB","ruBB-","ruB+","ruB","ruB-","ruCCC","ruCC","ruC","ruRD","ruD"]
fromNumbToNCR=["Неизвестно","AAA.ru","AA+.ru","AA.ru","AA-.ru","A+.ru","A.ru","A-.ru","BBB+.ru","BBB.ru","BBB-.ru","BB+.ru","BB.ru","BB-.ru","B+.ru","B.ru","B-.ru","CCC.ru","CC.ru","C.ru","D"]
fromNumbToNRA=["Неизвестно","AAA|ru|","AA+|ru|","AA|ru|","AA-|ru|","A+|ru|","A|ru|","A-|ru|","BBB+|ru|","BBB|ru|","BBB-|ru|","BB+|ru|","BB|ru|","BB-|ru|","B+|ru|","B|ru|","B-|ru|","CCC|ru|","CC|ru|","C|ru|","RD|ru|","SD|ru|","D|ru|"]


def calculate_ur_client_high_risk_zayceva(client: "UrClient") -> bool:
    k1 = client.str2300 / client.str1300
    k2 = client.str1520 / client.str1230
    k3 = (client.str1520 + client.str1510) / client.str1250
    k4 = client.str2300 / client.str2110
    k5 = (client.str1400 + client.str1500) / client.str1300
    k6 = client.str1600 / client.str2110
    k6_pred = client.str1600pred / client.str2110pred

    k_fact = 0.25 * k1 + 0.1 * k2 + 0.2 * k3 + 0.25 * k4 + 0.1 * k5 + 0.1 * k6
    k_norm = 1.57 + 0.1 * k6_pred

    return k_fact > k_norm


def calculate_ur_client_high_risk_saifullin(client: "UrClient") -> bool:
    k1 = (client.str1300 - client.str1100) / client.str1200
    k2 = client.str1200 / (client.str1520 + client.str1510 + client.str1550)
    k3 = 2 * client.str2110 / (client.str1600pred + client.str1600)
    k4 = client.str2400 / client.str2110
    k5 = client.str2400 / client.str1300

    R = 2 * k1 + 0.1 * k2 + 0.08 * k3 + 0.45 * k4 + k5

    return R < 1.0
