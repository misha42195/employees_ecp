# получение данных из файла клссификатора

# получение пути к файлу
# import os
# import xml.etree.ElementTree as et

# dower_path = os.path.abspath("assert/mchd_dower")  # получаем абсолютный путь от корня
# classifier_path = os.path.abspath("assert/mchd_dower")  # получаем абсолютный путь от корня


# from bs4 import BeautifulSoup


# # 1. Достаём коды полномочий из доверенности
# def get_cod_from_xml(xml_str):
#     soup = BeautifulSoup(xml_str, "xml")

#     code_list = [
#         el.get("КодПолн") for el in soup.find_all("МашПолн") if el.get("КодПолн")
#     ]
#     return code_list


# # 2. Парсим классификатор: сопоставление код → (код справочника, описание)
# def get_code_classifier(classifier_xml):
#     soup = BeautifulSoup(classifier_xml, "xml")
#     mapping = {}

#     for record in soup.find_all("nsi:record"):
#         code_full = None
#         code_power = None
#         description = None

#         for attr in record.find_all("nsi:attribute-value"):
#             ref = attr.get("attribute-ref")
#             val_node = attr.find("nsi:string") or attr.find("nsi:text")
#             if not val_node:
#                 continue

#             val = val_node.text.strip()

#             if ref == "ebf9c7b9-de51-4464-bace-bd35db701bf0":  # Код полномочия
#                 code_full = val
#             elif ref == "7f0f27ba-999f-4e22-af88-ac56997fdf39":  # Код справочника
#                 code_power = val
#             elif ref == "207ad289-389e-4bc7-8a3f-5dd9aef1e91e":  # Описание полномочия
#                 description = val

#         if code_full:
#             mapping[code_full] = {
#                 "code_power": code_power or "нет кода справочника",
#                 "description": description or "нет описания",
#             }

#     return mapping


# # 3. Сопоставляем и выводим всё
# def match_codes_classifier(dover_xml, classifier_xml):
#     dover_codes = get_cod_from_xml(dover_xml)
#     classifier_map = get_code_classifier(classifier_xml)

#     result = {}
#     for code in dover_codes:
#         entry = classifier_map.get(code)
#         if entry:
#             result[code] = entry
#         else:
#             result[code] = {
#                 "code_power": " не найден в классификаторе",
#                 "description": " не найдено описание",
#             }

#     return result


# Пример использования:
# with open("dover.xml", "r", encoding="utf-8") as f:
#     dover_xml = f.read()

# with open("classifier.xml", "r", encoding="utf-8") as f:
#     classifier_xml = f.read()

# matches = match_codes_classifier(dover_xml, classifier_xml)

# # Вывод
# for code, data in matches.items():
#     print(f"{code} → {data['code_power']}\n   📝 {data['description']}")


import os
import tempfile
from bs4 import BeautifulSoup


# 1. Достаём коды полномочий из доверенности
def get_cod_from_xml(xml_str_or_path):
    if os.path.exists(xml_str_or_path):
        with open(xml_str_or_path, "r", encoding="utf-8") as f:
            xml_str = f.read()
    else:
        xml_str = xml_str_or_path

    soup = BeautifulSoup(xml_str, "xml")
    code_list = [
        el.get("КодПолн") for el in soup.find_all("МашПолн") if el.get("КодПолн")
    ]
    return code_list



def get_code_classifier(classifier_xml_or_path,valid_codes):
    if os.path.exists(classifier_xml_or_path):
        with open(classifier_xml_or_path, "r", encoding="utf-8") as f:
            classifier_xml = f.read()
    else:
        classifier_xml = classifier_xml_or_path

    soup = BeautifulSoup(classifier_xml, "xml")
    mapping = {}

    for record in soup.find_all("nsi:record"):
        code_full = None
        code_power = None
        description = None

        for attr in record.find_all("nsi:attribute-value"):
            ref = attr.get("attribute-ref")
            val_node = attr.find("nsi:string") or attr.find("nsi:text")
            if not val_node:
                continue

            val = val_node.text.strip()

            if ref == "ebf9c7b9-de51-4464-bace-bd35db701bf0":  # Код полномочия
                code_full = val
            elif ref == "7f0f27ba-999f-4e22-af88-ac56997fdf39":  # Код справочника
                code_power = val
            elif ref == "207ad289-389e-4bc7-8a3f-5dd9aef1e91e":  # Описание полномочия
                description = val

        # Добавляем только если есть код полномочия и он в списке разрешённых
        if code_full and code_full in valid_codes:
            mapping[code_full] = {
                "code_full": code_full,
                "code_power": code_power or "нет кода справочника",
                "description": description or "нет описания",
            }

    return mapping

# 3. Сопоставляем и выводим всё
def match_codes_classifier(dover_codes, classifier_map)->dict:
    result = {}

    for code in dover_codes:
        entry = classifier_map.get(code)
        if entry:
            result[code] = {
                "code_full": code,
                "code_power": entry.get("code_power", "нет кода справочника"),
                "description": entry.get("description", "нет описания"),
            }
        else:
            result[code] = {
                "code_full": code,
                "code_power": "не найден в классификаторе",
                "description": "не найдено описание",
            }

    return result


"""
{'code_power': 'POWER_PWR_CLASS_MCHD_FK_EB10011', 'description': 'нет описания', 'code_full': 'FK9800_GIISEB_EB10011'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FK_EB10009', 'description': 'нет описания', 'code_full': 'FK9800_GIISEB_EB10009'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FK_EB10013', 'description': 'нет описания', 'code_full': 'FK9800_GIISEB_EB10013'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FK_EB10001', 'description': 'нет описания', 'code_full': 'FK9800_GIISEB_EB10001'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRANSAPPEALGENERAL', 'description': 'Подписывать обращения в Банк России', 'code_full': 'BRANSPPL_BRANSAPPEALGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRDEMANDGENERAL', 'description': 'Подписывать ответы на запросы/предписания Банка России', 'code_full': 'BRDMND_BRDEMANDGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRREPORTINGGENERAL', 'description': 'Подписывать отчетность и иную информацию, установленную нормативными актами Банка России, для представления в Банк России', 'code_full': 'BRREPTG_GNRL_BRREPORTINGGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRREPORTINGKYC', 'description': 'Подписывать информацию кредитной организации, направляемую в Банк России, в рамках работы сервиса "Знай своего клиента"', 'code_full': 'BRREPTG_KO_BRREPORTINGKYC'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRREPORTINGROSINKAS', 'description': 'Подписывать отчетность по форме 202-И Объединения "РОСИНКАС", установленную нормативными актами Банка России, для представления в Банк России', 'code_full': 'BRREPTG_ROSINC_BRREPORTINGROSINKAS'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRSTATREPORTINGNFOGNRL', 'description': 'Подписывать первичные статистические данные по формам федерального статистического наблюдения для представления в Банк России', 'code_full': 'BRREPTG_RSPND_BRSTATREPORTINGNFOGNRL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRDOCSGENERAL', 'description': 'Подписывать документы и иную информацию, установленную нормативными актами Банка России, для представления в Банк России', 'code_full': 'BRDOCS_GNRL_BRDOCSGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRSOURCEDOC1', 'description': 'Подписывать первичные учетные документы для представления в Банк России', 'code_full': 'BRDOCS_SRCDOC_BRSOURCEDOC1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRDOCUMENTSISSUER1', 'description': 'Подписывать документы, представляемые в Банк России для целей допуска на финансовый рынок эмиссионных ценных бумаг', 'code_full': 'BRDOCS_STCKDC_BRDOCUMENTSISSUER1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRDOCUMENTSKO1', 'description': 'Подписывать документы в рамках взаимодействия между кредитными организациями и Банком России при обмене информацией в рамках формирования пулов обеспечения по кредитам Банка России, состоящих из нерыночных активов', 'code_full': 'BRDOCS_KODOC_BRDOCUMENTSKO1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRDOCUMENTSKO2', 'description': 'Подписывать документы в рамках взаимодействия между кредитными организациями и Банком России при обмене информацией в рамках проведения депозитных и кредитных операций Банка России', 'code_full': 'BRDOCS_KODOC_BRDOCUMENTSKO2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRDOPUSKGENERAL', 'description': 'Подписывать документы, необходимые для прохождения процедур допуска, направляемые в Банк России', 'code_full': 'BRDPSK_BRDOPUSKGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRASVINFORMATION', 'description': 'Подписывать документы, содержащие информацию Государственной корпорации "Агентство по страхованию вкладов" об установлении дополнительных и повышенных дополнительных ставок страховых взносов в отношении кредитных организаций', 'code_full': 'BRASV_BRASVINFORMATION'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRGOZNAK', 'description': 'Подписывать информацию АО "Гознак", направляемую в Банк России', 'code_full': 'BRGZNK_BRGOZNAK'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRDOM.RF', 'description': 'Подписывать данные, передаваемые из Единой информационной системы жилищного строительства АО "ДОМ.РФ" в Банк России', 'code_full': 'BRDMRF_BRDOM.RF'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRPFRREPORTING', 'description': 'Представлять в Банк России отчетность и иную информацию в рамках взаимодействия с ПФР', 'code_full': 'BRPFR_BRPFRREPORTING'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRROSSTAT', 'description': 'Подписывать запросы и иную информацию, направляемую Росстатом в Банк России', 'code_full': 'BRRST_BRROSSTAT'}
{'code_power': 'POWER_PWR_CLASS_MCHD_CB_BRFNSREPORTING', 'description': 'Представлять в Банк России данные годовой бухгалтерской отчетности в рамках взаимодействия с ФНС России', 'code_full': 'BRFNS_BRFNSREPORTING'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_MIN01', 'description': 'Подписание кадровых документов от лица работодателя', 'code_full': 'MINTRUD_MIN01'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS14', 'description': 'Подписывать акт о приемке выполненных работ (КС-2)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS14'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUP1', 'description': 'Заключать и подписывать договоры на инкассацию платежных и расчетных документов', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUP1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUP2', 'description': 'Заключать и подписывать договоры на инкассацию денежных средств', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUP2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSBANK3', 'description': 'Подписывать акты выполнения работ', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_DOCSBANK3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTFCTRNG1', 'description': 'Заключать и подписывать договоры торгового и экспортного финансирования', 'code_full': 'BBDOCS_CNTRCT_SRVC_FCTRNG_CNTRCTFCTRNG1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT44', 'description': 'Заключать и подписывать договоры добровольного страхование имущества граждан (кроме страхования транспортных средств и сельскохозяйственного страхования)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT44'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTFCTRNGGENERAL', 'description': 'Заключать и подписывать договоры финансирования (факторинга)', 'code_full': 'BBDOCS_CNTRCT_SRVC_FCTRNG_CNTRCTFCTRNGGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT4', 'description': 'Заключать и подписывать договоры добровольного страхования средств наземного транспорта (кроме средств железнодорожного транспорта), за исключением автотранспортных средств', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT46', 'description': 'Заключать и подписывать договоры страхования домашнего имущества граждан', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT46'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT50', 'description': 'Заключать и подписывать договоры добровольного страхования имущества граждан в составе комбинированного (комплексного) договора ипотечного страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT50'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT29', 'description': 'Заключать и подписывать договоры страхования имущества юридических лиц (кроме страхования транспортных средств и сельскохозяйственного страхования) от всех рисков', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT29'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS9', 'description': 'Подписывать накладные на внутренние перемещение', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS9'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS20', 'description': 'Подписывать, направлять и получать акты о списании товарно-материальных ценностей (унифицированная форма № Торг-16)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS20'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTWRKGENERAL', 'description': 'Заключать и подписывать договоры выполнения работ', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTWRKGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT10', 'description': 'Заключать и подписывать договоры добровольного страхования средств водного транспорта', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT10'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS1', 'description': 'Подписывать отчет агента', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT28', 'description': 'Заключать и подписывать договоры страхования товаров на складе (кроме страхования транспортных средств и сельскохозяйственного страхования)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT28'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUP3', 'description': 'Заключать и подписывать договоры на оказание услуг по размену денежных средств', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUP3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS6', 'description': 'Подписывать товарные накладные', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS6'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK11', 'description': 'Заключать и подписывать договоры на выпуск карт и предоплаченных финансовых продуктов других эмитентов', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK11'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSBANK4', 'description': 'Подписывать списки и реестры на выпуск банковских карт', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_DOCSBANK4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS39', 'description': 'Подписывать и утверждать акты о списании объекта (групп объектов основных средств) и другие акты, предусмотренные внутренними нормативными документами', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS39'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC12', 'description': 'Заключать и подписывать договоры оказания услуг о предоставлении доступа к информации', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC12'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS19', 'description': 'Подписывать, направлять и получать акты о возврате товарно-материальных ценностей, сданных на хранение (унифицированная форма № МХ-3)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS19'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT43', 'description': 'Заключать и подписывать договоры страхования культурных ценностей', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT43'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS12', 'description': 'Подписывать иные накладные', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS12'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS30', 'description': 'Подписывать расчетные документы', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS30'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSFCTRNGGENERAL', 'description': 'Подписывать документы, связанные с исполнением/неисполнением обязательств по договорам финансирования (факторинга)', 'code_full': 'BBDOCS_CNTRCT_SRVC_FCTRNG_DOCSFCTRNGGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_ADDTNLCNTRCTFCTRNGGENERAL', 'description': 'Заключать и подписывать к договорам финансирования (факторинга), приложения, спецификации, дополнительные соглашения (соглашения) об их изменении, расторжении и прекращении', 'code_full': 'BBDOCS_CNTRCT_SRVC_FCTRNG_ADDTNLCNTRCTFCTRNGGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSBANK2', 'description': 'Подписывать акты об оказании услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_DOCSBANK2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSFCTRNG1', 'description': 'Подписывать акты об оказании услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_FCTRNG_DOCSFCTRNG1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK2', 'description': 'Заключать и подписывать договоры присоединения к Правилам платежной системы в качестве члена платежной системы', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBACCNT7', 'description': 'Заключать и подписывать договоры специального банковского счета', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_CNTRCTBACCNT7'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK17', 'description': 'Заключать, исполнение договора об оказании информационных услуг с бюро кредитных историй', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK17'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC4', 'description': 'Заключать и подписывать договоры на оказания услуг по ведению бухгалтерского и налогового учета', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT3', 'description': 'Заключать и подписывать договоры добровольного страхования автотранспортных средств', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT13', 'description': 'Заключать и подписывать договоры страхования ценных грузов', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT13'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSBACCNT1', 'description': 'Распоряжаться денежными средствами на банковских счетах', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_DOCSBACCNT1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS13', 'description': 'Подписывать справки о стоимости выполненных работ и затрат (КС-3)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS13'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSBACCNT4', 'description': 'Подписывать, направлять документы, связанные с исполнением/неисполнением, изменение обязательств по договорам дистанционного банковского обслуживания, расторжением договора дистанционного банковского обслуживания', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_DOCSBACCNT4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT45', 'description': 'Заключать и подписывать договоры страхования строений граждан', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT45'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVCGENERAL', 'description': 'Заключать и подписывать договоры оказания услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVCGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUP10', 'description': 'Заключать и подписывать договоры на доставку и перевозку драгоценных металлов', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUP10'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS5', 'description': 'Подписывать товарные, товарно-транспортные, транспортные накладные, универсальные передаточные документы (УПД)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS5'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTFCTRNG2', 'description': 'Заключать и подписывать договоры проектного финансирования', 'code_full': 'BBDOCS_CNTRCT_SRVC_FCTRNG_CNTRCTFCTRNG2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS10', 'description': 'Подписывать накладные на отпуск материалов на сторону,', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS10'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC15', 'description': 'Заключать и подписывать соглашения об электронном документообороте', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC15'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSPRPRT7', 'description': 'Подписывать, направлять документы, связанных с реализацией страховой организацией годных остатков имущества, поступившего в собственность страховой организации после осуществления страховой выплаты, третьим лицам', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_DOCSPRPRT7'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSPRPRT5', 'description': 'Подписывать распоряжения на страховые выплаты', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_DOCSPRPRT5'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUP5', 'description': 'Заключать и подписывать договоры на доставку и перевозку ценных бумаг', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUP5'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC2', 'description': 'Заключать и подписывать договоры возмездного оказания услуг с самозанятыми', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT33', 'description': 'Заключать и подписывать договоры страхования имущества юридических лиц от риска утраты в результате прекращения права собственности и других вещных прав на недвижимое имущество (титула собственности)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT33'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK7', 'description': 'Заключать и подписывать договоры на выпуск зарплатных/корпоративных банковских карт', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK7'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK19', 'description': 'Заключать и подписывать договоры в рамках участия в платежных системах', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK19'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT2', 'description': 'Заключать и подписывать договоры добровольного страхования средств наземного транспорта (кроме средств железнодорожного транспорта)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT6', 'description': 'Заключать и подписывать договоры добровольного страхования средств железнодорожного транспорта', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT6'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT48', 'description': 'Заключать и подписывать договоры страхования персональных электронных устройств и бытовой техники', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT48'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS4', 'description': 'Подписывать и оплачивать счета на оплату товаров (работ, услуг)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT24', 'description': 'Заключать и подписывать договоры страхования сельскохозяйственных животных, осуществляемого с государственной поддержкой', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT24'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUP7', 'description': 'Заключать и подписывать договоры на инкассацию иных ценностей', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUP7'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK6', 'description': 'Заключать и подписывать договоры на расчетно-кассовое обслуживание физических лиц', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK6'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT49', 'description': 'Заключать и подписывать добровольного страхования имущества граждан от риска утраты в результате прекращения права собственности и других вещных прав на недвижимое имущество (титула собственности)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT49'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS8', 'description': 'Подписывать транспортные накладные', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS8'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSBACCNT2', 'description': 'Подписывать, направлять документы, связанные с исполнением/неисполнением, изменение обязательств по договорам банковского счета, расторжением договора банковского счета', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_DOCSBACCNT2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT8', 'description': 'Заключать и подписывать договоры добровольного страхования средств воздушного транспорта', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT8'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS28', 'description': 'Подписывать, направлять и получать справки о товарообороте', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS28'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSWRK1', 'description': 'Подписывать акты выполнения работ', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_DOCSWRK1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC5', 'description': 'Заключать и подписывать договоры на оказания услуг по учету товародвижения и долгосрочному хранению документов', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC5'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS36', 'description': 'Подписывать передаточные распоряжения', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS36'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_ADDTNLCNTRCTBANKGENERAL', 'description': 'Заключать и подписывать к договорам банковских услуг, приложения, спецификации, дополнительные соглашения (соглашения) об их изменении, расторжении и прекращении', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_ADDTNLCNTRCTBANKGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUP9', 'description': 'Заключать и подписывать договоры на доставку и перевозку валюты', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUP9'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT32', 'description': 'Заключать и подписывать договоры страхования от огня и других опасностей промышленных и коммерческих предприятий, учреждений и организаций', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT32'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT39', 'description': 'Заключать и подписывать договоры добровольного страхования имущества юридических лиц: авиационной техники на простое (в постройке, ремонте)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT39'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT30', 'description': 'Заключать и подписывать договоры страхования специализированной техники, производственных передвижных и самоходных машин и иного оборудования (кроме страхования транспортных средств и сельскохозяйственного страхования)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT30'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT40', 'description': 'Заключать и подписывать договоры страхования имущества кредитных организаций (банков) в составе комбинированного (комплексного) договора страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT40'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTFCTRNG4', 'description': 'Заключать и подписывать договоры финансирования под уступку денежного требования (факторинг), включая договоры международного факторинга', 'code_full': 'BBDOCS_CNTRCT_SRVC_FCTRNG_CNTRCTFCTRNG4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSPICKUP1', 'description': 'Подписывать акты об оказании услуг', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_DOCSPICKUP1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTFCTRNG3', 'description': 'Заключать и подписывать договоры финансирования под уступку денежного требования (факторинг)', 'code_full': 'BBDOCS_CNTRCT_SRVC_FCTRNG_CNTRCTFCTRNG3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC17', 'description': 'Заключать, подписывать, изменять, расторгать соглашения о партнерстве и сотрудничестве', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC17'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS25', 'description': 'Подписывать, направлять и получать акты о списании товаров, акт о порче, бое, ломе товарно-материальных ценностей, сличительную ведомость результатов инвентаризации товарно-материальных ценностей, расчет естественной убыли на реализованные товары', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS25'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT19', 'description': 'Заключать и подписывать договоры страхования объектов товарной аквакультуры (товарного рыбоводства)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT19'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSPRPRTGENERAL', 'description': 'Подписывать документы, связанные с исполнением/неисполнением обязательств по договорам имущественного страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_DOCSPRPRTGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_ADDTNLCNTRCTPICKUPGENERAL', 'description': 'Заключать и подписывать к договорам инкассации приложения, спецификации, дополнительные соглашения (соглашения) об их изменении, расторжении и прекращении', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_ADDTNLCNTRCTPICKUPGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSPRPRT4', 'description': 'Подписывать акты о страховых случаях', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_DOCSPRPRT4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT37', 'description': 'Заключать и подписывать договоры комплексного страхования строительно-монтажных работ от всех рисков', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT37'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT22', 'description': 'Заключать и подписывать договоры страхования урожая сельскохозяйственных культур, осуществляемого с государственной поддержкой', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT22'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS15', 'description': 'Подписывать акт списания основных средств', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS15'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUP8', 'description': 'Заключать и подписывать договоры на доставку и перевозку иных ценностей', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUP8'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT15', 'description': 'Заключать и подписывать договоры добровольного сельскохозяйственного страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT15'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS23', 'description': 'Подписывать, направлять и получать уведомление о приемке товара на склад (RECADV)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS23'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK14', 'description': 'Заключать и подписывать договоры на осуществление деятельности оператора услуг платежной инфраструктуры', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK14'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRTGENERAL', 'description': 'Заключать и подписывать договоры имущественного страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRTGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC19', 'description': 'Заключать, подписывать, изменять, расторгать соглашения о гарантиях и заверениях', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC19'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC10', 'description': 'Заключать и подписывать договоры об оказании консультационных услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC10'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT51', 'description': 'Заключать и подписывать договоры добровольного страхования имущества граждан в составе комбинированного (комплексного) договора страхования авиапассажиров', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT51'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS35', 'description': 'Подписывать и предъявлять к оплате любые финансовые документы', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS35'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUP4', 'description': 'Заключать и подписывать договоры на инкассацию ценных бумаг', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUP4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC3', 'description': 'Заключать и подписывать договоры о передаче полномочий единоличного исполнительного органа управляющей организации', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBACCNT1', 'description': 'Заключать и подписывать договоры открытия банковского счета', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_CNTRCTBACCNT1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK18', 'description': 'Заключать и подписывать соглашения о размещении средств страховых взносов на финансирование накопительной части трудовой пенсии, поступивших в течение финансового года в Социальный фонд России, на депозитах в валюте Российской Федерации', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK18'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS26', 'description': 'Подписывать, направлять и получать спецификации, акты расчета вознаграждения (премии)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS26'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT47', 'description': 'Заключать и подписывать договоры страхования имущества граждан и дополнительных рисков в составе комбинированного (комплексного) договора страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT47'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBACCNT8', 'description': 'Заключать и подписывать соглашения о порядке начисления процентов на остаток денежных средств на счете', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_CNTRCTBACCNT8'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT25', 'description': 'Заключать и подписывать договоры страхования объектов товарной аквакультуры (товарного рыбоводства), осуществляемого с государственной поддержкой', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT25'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK12', 'description': 'Заключать и подписывать договоры на участие в платежных системах', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK12'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT27', 'description': 'Заключать и подписывать договоры добровольного страхования имущества юридических лиц (кроме страхования транспортных средств и сельскохозяйственного страхования)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT27'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSPRPRT1', 'description': 'Подписывать документы, связанные с отказом в страховой выплате', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_DOCSPRPRT1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT54', 'description': 'Заключать и подписывать договоры добровольного страхования имущества граждан: водного транспорта малого тоннажа', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT54'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS3', 'description': 'Подписывать и оплачивать счета на оплату работ (услуг)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT11', 'description': 'Заключать и подписывать договоры страхования средств водного транспорта в составе комбинированного (комплексного) договора страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT11'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS34', 'description': 'Подписывать и оплачивать чеки', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS34'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCSGENERAL', 'description': 'Подписывать, направлять, получать и оплачивать бухгалтерские документы', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCSGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSBACCNT3', 'description': 'Подписывать, направлять документы, связанные с исполнением/неисполнением, изменение обязательств по договорам эквайринга, расторжением договора эквайринга', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_DOCSBACCNT3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK5', 'description': 'Заключать и подписывать договоры на расчетно-кассовое обслуживание юридических лиц', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK5'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSPRPRT6', 'description': 'Подписывать запросы и иные документы, адресованные третьим лицам касательно взыскания страховой организацией денежных средств в порядке суброгации и регресса', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_DOCSPRPRT6'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSBANK1', 'description': 'Заключать, изменять, расторгать договоры на оказание услуг в рамках зарплатного/социального проекта, а также подписывать иные документы в рамках данных договоров', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_DOCSBANK1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT35', 'description': 'Заключать и подписывать договоры страхования имущества, используемого при проведении строительно-монтажных работ', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT35'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK4', 'description': 'Заключать и подписывать договоры на осуществление переводов денежных средств физических лиц', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS7', 'description': 'Подписывать товарно-транспортные накладные', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS7'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT26', 'description': 'Заключать и подписывать договоры страхования урожая сельскохозяйственных культур, посадок многолетних насаждений, осуществляемого с государственной поддержкой, на случай чрезвычайных ситуаций природного характера', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT26'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC16', 'description': 'Заключать, подписывать, изменять, расторгать соглашения о намерениях', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC16'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT21', 'description': 'Заключать и подписывать договоры добровольного сельскохозяйственного страхования, осуществляемого с государственной поддержкой', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT21'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSSRVCWRKGENERAL', 'description': 'Подписывать, направлять документы, связанные с исполнением/неисполнением обязательств по договорам оказания услуг/работ, предъявлять замечания и претензии по качеству, срокам и объемам выполненных работ/оказанных услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_DOCSSRVCWRKGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC6', 'description': 'Заключать и подписывать договоры по оказанию услуг кадрового делопроизводства', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC6'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT31', 'description': 'Заключать и подписывать договоры страхования контейнеров', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT31'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUP6', 'description': 'Заключать и подписывать договоры на инкассацию ценностей', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUP6'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT16', 'description': 'Заключать и подписывать договоры страхования урожая сельскохозяйственных культур', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT16'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_ADDTNLCNTRCTBACCNTGENERAL', 'description': 'Заключать и подписывать к договорам банковского счета приложения, спецификации, дополнительные соглашения (соглашения) об их изменении, расторжении и прекращении', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_ADDTNLCNTRCTBACCNTGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBACCNT6', 'description': 'Заключать и подписывать соглашения о лимите дебетового остатка', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_CNTRCTBACCNT6'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_ADDTNLCNTRCTPRPRTGENERAL', 'description': 'Заключать и подписывать к договорам имущественного страхования приложения, спецификации, дополнительные соглашения (соглашения) об их изменении, расторжении и прекращении', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_ADDTNLCNTRCTPRPRTGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT5', 'description': 'Заключать и подписывать договоры страхования средств наземного транспорта (кроме средств железнодорожного транспорта) в составе комбинированного (комплексного) договора страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT5'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSSRVC1', 'description': 'Подписывать акты об оказании услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_DOCSSRVC1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT17', 'description': 'Заключать и подписывать договоры страхования посадок многолетних насаждений', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT17'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBACCNT5', 'description': 'Заключать и подписывать договоры эквайринга', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_CNTRCTBACCNT5'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS11', 'description': 'Подписывать международные товарные (товарно-транспортные) накладные CMR', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS11'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT14', 'description': 'Заключать и подписывать договоры страхования грузов и от убытков при задержке в доставке груза в составе комбинированного (комплексного) договора страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT14'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC7', 'description': 'Заключать и подписывать договоры об оказании IT услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC7'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT1', 'description': 'Заключать и подписывать соглашения об урегулировании страховых случаев по договорам имущественного страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK10', 'description': 'Заключать и подписывать договоры на выпуск карт российских платежных систем', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK10'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSBACCNTGENERAL', 'description': 'Подписывать документы, связанные с исполнением/неисполнением обязательств по договорам банковского счета', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_DOCSBACCNTGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT38', 'description': 'Заключать и подписывать договоры добровольного страхования имущества юридических лиц: судов на простое (в постройке, ремонте)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT38'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT7', 'description': 'Заключать и подписывать договоры страхования средств железнодорожного транспорта в составе комбинированного (комплексного) договора страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT7'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT18', 'description': 'Заключать и подписывать договоры страхования сельскохозяйственных животных', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT18'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS21', 'description': 'Подписывать, направлять и получать акты о бое, порче, ломе товарно-материальных ценностей (унифицированная форма №Торг-15)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS21'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC11', 'description': 'Заключать и подписывать договоры об оказании юридических услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC11'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT42', 'description': 'Заключать и подписывать договоры страхования музейных предметов', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT42'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSPRPRT3', 'description': 'Подписывать расчеты сумм ущерба, причиненного страховыми случаями', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_DOCSPRPRT3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBACCNTGENERAL', 'description': 'Заключать и подписывать договоры банковского счета', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_CNTRCTBACCNTGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK13', 'description': 'Заключать и подписывать договоры об условиях и порядке обмена документами в электронном виде с использованием Системы передачи финансовых сообщений Банка России', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK13'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS24', 'description': 'Подписывать, направлять и получать кассовые документы и подтверждающие расходы документы (приходный кассовый ордер, расходный кассовый ордер, кассовую книгу, платежные ведомости, карточки депонентов)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS24'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBACCNT9', 'description': 'Заключать и подписывать договоры на расчетно-кассовое обслуживание', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_CNTRCTBACCNT9'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSPICKUPGENERAL', 'description': 'Подписывать документы, связанные с исполнением/неисполнением обязательств по договорам инкассации', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_DOCSPICKUPGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBACCNT3', 'description': 'Заключать и подписывать договоры открытия специальных счетов', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_CNTRCTBACCNT3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS32', 'description': 'Подписывать и предъявлять к оплате платежные поручения', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS32'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_ADDTNLCNTRCTSRVCWRKGENERAL', 'description': 'Заключать и подписывать к договорам услуг/работ, спецификации, дополнительные соглашения (соглашения) об их изменении, расторжении и прекращении', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_ADDTNLCNTRCTSRVCWRKGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS33', 'description': 'Подписывать и предъявлять к оплате инкассовые поручения', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS33'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC1', 'description': 'Заключать и подписывать договоры оказания услуг по обеспечению безопасности с использованием комплекса тревожной сигнализации', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK16', 'description': 'Заключать и подписывать договоры на изготовление для кредитной организации аффинажной организацией драгоценных металлов в виде слитков', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK16'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT20', 'description': 'Заключать и подписывать договоры страхования имущества сельскохозяйственных товаропроизводителей, заемщиков по договорам кредита (займа)', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT20'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK8', 'description': 'Заключать и подписывать договоры на выпуск, распространение и обслуживание платежных карт', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK8'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS27', 'description': 'Подписывать, направлять и получать акты зачета взаимных требований', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS27'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT34', 'description': 'Заключать и подписывать договоры страхования имущества юридических лиц (кроме страхования транспортных средств и сельскохозяйственного страхования) от рисков при проведении строительно-монтажных работ', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT34'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC13', 'description': 'Заключать и подписывать договоры оказания услуг технической поддержки (технического сопровождения)', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC13'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANKGENERAL', 'description': 'Заключать и подписывать договоры банковских услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANKGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT52', 'description': 'Заключать и подписывать договоры добровольного страхования имущества граждан в составе комбинированного (комплексного) договора страхования пассажиров', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT52'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSBANKGENERAL', 'description': 'Подписывать документы, связанные с исполнением/неисполнением обязательств по договорам банковских услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_DOCSBANKGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSPRPRT2', 'description': 'Подписывать запросы о предоставлении дополнительных документов и информации, а также связанных с изменением сроков урегулирования убытков', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_DOCSPRPRT2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK3', 'description': 'Заключать и подписывать договоры на осуществление переводов денежных средств юридических лиц', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC8', 'description': 'Заключать и подписывать договоры на оказания казначейских услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC8'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK9', 'description': 'Заключать и подписывать договоры на выпуск международных платежных карт', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK9'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT53', 'description': 'Заключать и подписывать договоры добровольного страхования имущества граждан в составе комбинированного (комплексного) договора страхования средств водного транспорта', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT53'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS31', 'description': 'Подписывать и предъявлять к оплате счета', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS31'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS29', 'description': 'Подписывать, направлять и получать бухгалтерские справки', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS29'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_ADDTNLCNTRCTCCGENERAL', 'description': 'Заключать и подписывать к договорам услуг/работ с Удостоверяющем центром, спецификации, дополнительные соглашения (соглашения) об их изменении, расторжении и прекращении', 'code_full': 'BBDOCS_CNTRCT_SRVC_СС_ADDTNLCNTRCTCCGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBANK15', 'description': 'Заключать и подписывать договоры между участниками электронного взаимодействия (в том числе, в соответствии с правилами платежных систем)', 'code_full': 'BBDOCS_CNTRCT_SRVC_BANK_CNTRCTBANK15'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT12', 'description': 'Заключать и подписывать договоры добровольного страхования грузов', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT12'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPICKUPGENERAL', 'description': 'Заключать и подписывать договоры инкассации', 'code_full': 'BBDOCS_CNTRCT_TRFFC_PICKUP_CNTRCTPICKUPGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT9', 'description': 'Заключать и подписывать договоры страхования средств воздушного транспорта в составе комбинированного (комплексного) договора страхования', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT9'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT36', 'description': 'Заключать и подписывать договоры комплексного страхования строительно-монтажных работ', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT36'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS17', 'description': 'Подписывать журнал вызова технического специалиста', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS17'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTPRPRT23', 'description': 'Заключать и подписывать договоры страхования посадок многолетних насаждений, осуществляемого с государственной поддержкой', 'code_full': 'BBDOCS_CNTRCT_INSRNC_PRPRT_CNTRCTPRPRT23'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBACCNT4', 'description': 'Заключать и подписывать договоры на оказание услуг по дистанционному обслуживанию клиентов', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_CNTRCTBACCNT4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_SOURCEDOCS22', 'description': 'Подписывать, направлять и получать акты о расхождении при приемке товарно-материальных ценностей (унифицированная форма № Торг-2, Торг-3)', 'code_full': 'BBDOCS_DOCS_DCSALL_SRCDOC_SOURCEDOCS22'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTBACCNT2', 'description': 'Заключать и подписывать договоры корреспондентского счета (субсчета)', 'code_full': 'BBDOCS_CNTRCT_ACCNT_BACCNT_CNTRCTBACCNT2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTSRVC14', 'description': 'Заключать и подписывать договоры оказания услуг о предоставлении доступа к программам для ЭВМ и (или) базам данных', 'code_full': 'BBDOCS_CNTRCT_SRVC_SRVCWRK_CNTRCTSRVC14'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB33', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB33'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB17', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB17'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB40', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB40'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB14', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB14'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB43', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB43'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB48', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB48'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB9', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB9'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB50', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB50'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB47', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB47'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB7', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB7'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB38', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB38'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB8', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB8'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB51', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB51'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB63', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB63'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB30', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB30'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB19', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB19'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB32', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB32'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB41', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB41'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB57', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB57'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB49', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB49'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB59', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB59'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB42', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB42'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB24', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB24'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB11', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB11'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB12', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB12'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB39', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB39'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB21', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB21'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB25', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB25'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB36', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB36'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB46', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB46'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB2', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB20', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB20'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB15', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB15'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB35', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB35'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB13', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB13'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB23', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB23'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB53', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB53'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB29', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB29'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB56', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB56'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB1', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB61', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB61'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB28', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB28'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB55', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB55'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB64', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB64'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB18', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB18'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB16', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB16'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB44', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB44'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB6', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB6'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB58', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB58'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB22', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB22'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB37', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB37'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB45', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB45'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_REB34', 'description': 'нет описания', 'code_full': 'MEFMO_GISREB_REB34'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTСС3', 'description': 'Заключать, подписывать, изменять, расторгать соглашения, направленные на создание и проверку сертификатов ключей аутентификации электронной подписи', 'code_full': 'BBDOCS_CNTRCT_SRVC_СС_CNTRCTСС3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSСС4', 'description': 'Подписывать акты выполнения работ', 'code_full': 'BBDOCS_CNTRCT_SRVC_СС_DOCSСС4'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSСС2', 'description': 'Подписывать акты приема-передачи средств криптографической защиты информации и шифрования', 'code_full': 'BBDOCS_CNTRCT_SRVC_СС_DOCSСС2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTССGENERAL', 'description': 'Заключать и подписывать договоры оказания услуг с Удостоверяющем Центром', 'code_full': 'BBDOCS_CNTRCT_SRVC_СС_CNTRCTССGENERAL'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSСС1', 'description': 'Подписывать документы и совершать действия, направленные на реализацию договоров (соглашений), включая обмен сертификатами ключами аутентификации подписей, ключами доступа, паролями, шифрами', 'code_full': 'BBDOCS_CNTRCT_SRVC_СС_DOCSСС1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTСС1', 'description': 'Заключать и подписывать договоры поручения о выдачи квалифицированных сертификатов ключа проверки электронной подписи', 'code_full': 'BBDOCS_CNTRCT_SRVC_СС_CNTRCTСС1'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_CNTRCTСС2', 'description': 'Заключать и подписывать договоры оказания услуг по хранению электронных доверенностей', 'code_full': 'BBDOCS_CNTRCT_SRVC_СС_CNTRCTСС2'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ANOTHER_DOCSСС3', 'description': 'Подписывать акты об оказании услуг', 'code_full': 'BBDOCS_CNTRCT_SRVC_СС_DOCSСС3'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FGISOPVK_FGISOPVK-01', 'description': '@FGISOPVK-01@ заключать и подписывать в ФГИС ОПВК договоры, дополнительные соглашения, изменять, расторгать договоры, подписывать акты и иные документы во исполнение заключенных договоров', 'code_full': '@FGISOPVK-01@'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FGISOPVK_FGISOPVK-02', 'description': '@FGISOPVK-02@ направлять и подписывать в ФГИС ОПВК заявки на вывоз отходов', 'code_full': '@FGISOPVK-02@'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FGISOPVK_FGISOPVK-06', 'description': '@FGISOPVK-06@ направлять и подписывать в ФГИС ОПВК протоколы по выбору исполнителя услуг (протоколы выбора оператора)', 'code_full': '@FGISOPVK-06@'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FGISOPVK_FGISOPVK-03', 'description': '@FGISOPVK-03@ представлять и подписывать в ФГИС ОПВК уведомления, информацию, документы, необходимые для регистрации и работе в личном кабинете ФГИС ОПВК', 'code_full': '@FGISOPVK-03@'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FGISOPVK_FGISOPVK-04', 'description': '@FGISOPVK-04@ направлять и подписывать в ФГИС ОПВК предложение оператора по обращению с отходами I и II классов опасности на оказание услуг', 'code_full': '@FGISOPVK-04@'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FGISOPVK_FGISOPVK-05', 'description': '@FGISOPVK-05@ направлять и подписывать в ФГИС ОПВК поручения на оказание услуг, направляемые операторам по обращению с отходами I и II классов опасности', 'code_full': '@FGISOPVK-05@'}
{'code_power': 'POWER_PWR_CLASS_MCHD_RFM_RFM001', 'description': 'нет описания', 'code_full': '1_RFM01'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FBMSE_FBMSE001', 'description': 'Подписание уполномоченным лицом за руководителя ГБ/ФБ документов медико-социальной экспертизы (в случае назначения заместителя руководителя на должность исполняющего обязанности руководителя)', 'code_full': '1_FBMSE01'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FBMSE_FBMSE003', 'description': 'нет описания', 'code_full': '1_FBMSE03'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FBMSE_FBMSE006', 'description': 'Подписание психологом (уполномоченным лицом за психолога) документов медико-социальной экспертизы', 'code_full': '1_FBMSE06'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FBMSE_FBMSE005', 'description': 'Подписание специалистом по реабилитации инвалидов (уполномоченным лицом за специалиста по реабилитации инвалидов) документов медико-социальной экспертизы', 'code_full': '1_FBMSE05'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FBMSE_FBMSE007', 'description': 'Подписание специалистом по социальной работе (уполномоченным лицом за специалиста по социальной работе) документов медико-социальной экспертизы', 'code_full': '1_FBMSE07'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FBMSE_FBMSE004', 'description': 'Подписание врачом по медико-социальной экспертизе (врач по МСЭ) (уполномоченным лицом за врача по МСЭ) документов медико-социальной экспертизы', 'code_full': '1_FBMSE04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_FBMSE_FBMSE002', 'description': 'Подписание руководителем (уполномоченным лицом за руководителя либо и.о. руководителя) бюро документов медико-социальной экспертизы', 'code_full': '1_FBMSE02'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P087-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P087-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P096-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P096-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P009-R04', 'description': 'Доступ к Единому регистру пользователей', 'code_full': 'ROSSTAT_P009-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P076-R04', 'description': '-', 'code_full': 'ROSSTAT_P076-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P086-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P086-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P026-R04', 'description': 'Отслеживание оплаты штрафа по постановлению по делу об АП о назначнии административного наказания', 'code_full': 'ROSSTAT_P026-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P003-R04', 'description': 'Доступ к согласованию заявок', 'code_full': 'ROSSTAT_P003-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P048-R04', 'description': 'Полномочие предоставляет возможность доступа к журналу входящих документов из ФПСР; к  справочнику форм и показателей;  к реестру форм и показателей', 'code_full': 'ROSSTAT_P048-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P024-R04', 'description': 'Рассмотрение жалоб по делу об административном правонарушении', 'code_full': 'ROSSTAT_P024-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P090-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P090-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P030-R04', 'description': 'Возбуждение исполнительного производства', 'code_full': 'ROSSTAT_P030-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P032-R04', 'description': 'Формирование протокола об админ. правонарушении', 'code_full': 'ROSSTAT_P032-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P114-R04', 'description': '-', 'code_full': 'ROSSTAT_P114-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P097-R04', 'description': 'Подписание соглашения об использовании простой электронной подписи', 'code_full': 'ROSSTAT_P097-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P038-R04', 'description': 'Формирование заявок на внесение изменений в состав справочников', 'code_full': 'ROSSTAT_P038-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P034-R04', 'description': 'Формирование протокола об админ. правонарушении', 'code_full': 'ROSSTAT_P034-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P050-R04', 'description': 'Полномочие предоставляет возможность доступа к реестру расписаний', 'code_full': 'ROSSTAT_P050-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P117-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P117-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P099-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P099-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P007-R04', 'description': 'Доступ к Реестре доверенностей МФЗР', 'code_full': 'ROSSTAT_P007-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P094-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P094-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P119-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P119-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P091-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P091-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P052-R04', 'description': 'Полномочие предоставляет возможность доступа к реестру расписаний', 'code_full': 'ROSSTAT_P052-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P078-R04', 'description': '-', 'code_full': 'ROSSTAT_P078-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P001-R04', 'description': 'Доступ к Реестре заявок на регистрацию пользователей', 'code_full': 'ROSSTAT_P001-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P008-R04', 'description': 'Доступ к Реестру заявок на регистрацию пользователей', 'code_full': 'ROSSTAT_P008-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P014-R04', 'description': 'Рассмотрение дела об административных правонарушениях в сфере официального статистического учета', 'code_full': 'ROSSTAT_P014-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P016-R04', 'description': 'Рассмотрение ходатайств/заявлений по делу об административном правонарушении', 'code_full': 'ROSSTAT_P016-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P075-R04', 'description': '-', 'code_full': 'ROSSTAT_P075-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P022-R04', 'description': 'Формирование документов и сообщений в рамках админ. производства', 'code_full': 'ROSSTAT_P022-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P046-R04', 'description': 'Полномочие предоставляет возможность доступа к журналу входящих документов из ФПСР; к  справочнику форм и показателей; к реестру форм и показателей', 'code_full': 'ROSSTAT_P046-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P085-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P085-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P074-R04', 'description': '-', 'code_full': 'ROSSTAT_P074-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P012-R04', 'description': 'Формирование протокола об административных правонарушениях', 'code_full': 'ROSSTAT_P012-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P116-R04', 'description': '-', 'code_full': 'ROSSTAT_P116-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P036-R04', 'description': 'Ведение справочников АП', 'code_full': 'ROSSTAT_P036-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P018-R04', 'description': 'Предоставление сведений по запросу по делу об административном правонарушении', 'code_full': 'ROSSTAT_P018-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P122-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P122-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P092-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P092-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P120-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P120-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P004-R04', 'description': 'Доступ к справочной информации МФЗР', 'code_full': 'ROSSTAT_P004-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P089-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P089-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P006-R04', 'description': 'Доступ к администрированию компонентов МФЗР', 'code_full': 'ROSSTAT_P006-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P080-R04', 'description': '-', 'code_full': 'ROSSTAT_P080-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P093-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P093-R04'}
{'code_power': 'POWER_PWR_CLASS_MCHD_ROSSTAT_P088-R04', 'description': 'нет описания', 'code_full': 'ROSSTAT_P088-R04'}
"""
