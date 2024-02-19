import os
from os import path
import sys
# 支付相关：支付（pay、payment、paid、charge） 购买（buy、purchase）  价格（price、tariff） 钱（money、coin)
# 聊天相关：聊天（chat、talk、speak、say） 连麦（link、connect）

pay_word = ['pay','payment','paid','charge','buy','purchase','price','money','coin']
chat_word = ['chat','talk','link']
sensitive_word = ['itms-services','付费语音','提现','weixinpay','wechatpay','alipay','unionpay','jdpay','paychat','pay_chat','chatpayment','钻/分钟','hotupdate','hotupdating','hotfix','cocosupdate','cocosfix','dynamicfix']

# pay_word = ['hot','dynamic','cocos']
# chat_word = ['update','updating','patch','patching','fix','repair','repairing']
# ignore_word = ['dispatch','@dynamic','photo','mas_updateConstraints:','hasPrefix:','hasSuffix:','snapshot','screenshot']

def scaner_file(url,result_url):

    file = os.listdir(url)
    for f in file:
        real_url = path.join(url, f)
        if path.isfile(real_url):
            file_name = path.abspath(real_url)
            if file_name.endswith('.m') or file_name.endswith('.h'):
                try:
                    anversion = open(file_name, "rt")
                    target_pay_word = []
                    target_chat_word = []
                    target_sensitive_word = []
                    for line in anversion:
                        if line.startswith('//'):   
                            continue
                        for _pay_word in pay_word:
                            if str(line).lower().__contains__(_pay_word):
                                if not target_pay_word.__contains__(_pay_word):
                                    target_pay_word.append(_pay_word)
                                # print(file_name)
                                # print(line)

                        for _chat_word in chat_word:
                            if str(line).lower().__contains__(_chat_word) :
                                if not target_chat_word.__contains__(_chat_word):
                                    target_chat_word.append(_chat_word)
                                # print(file_name)
                                # print(line)

                        for _sensitive_word in sensitive_word:
                            if str(line).lower().__contains__(_sensitive_word):
                                if not target_sensitive_word.__contains__(_sensitive_word):
                                    target_sensitive_word.append(_sensitive_word)
                                # print(file_name)
                                # print(line)

                    anversion.close()

                    # os.path.basename(file_name) 获取最后一个文件夹名      os.path.dirname(file_name) 获取文件路径
                    _file_name = file_name.split('/')[-1]

                    all_class_path = path.join(result_url, 'all_class_filter.txt')

                    file_handler = open(all_class_path, 'a+', encoding="utf-8")
                    for chat_file_name in target_chat_word:
                        for pay_file_name in target_pay_word:
                            class_name = _file_name+'_'+chat_file_name+'_'+pay_file_name
                            # print(class_name)
                            file_handler.writelines(class_name)
                            file_handler.write('\n')
                    for chat_file_name in target_chat_word:
                        for pay_file_name in target_pay_word:
                            class_name = _file_name + '_' + chat_file_name + '_' + pay_file_name
                            # print(class_name)
                            file_handler.writelines(class_name)
                            file_handler.write('\n')
                    for sensitive_file_word in target_sensitive_word:
                        class_name = _file_name + '_' + sensitive_file_word
                        # print(class_name)
                        file_handler.writelines(class_name)
                        file_handler.write('\n')
                                
                    file_handler.close()


                    # sensitive_class_path = path.join(result_url, 'sensitive_word_filter.txt')
                    # sensitive_file_handler = open(sensitive_class_path, 'a+', encoding="utf-8")

                    # for sensitive_file_word in target_sensitive_word:
                    #     class_name = _file_name + '_' + sensitive_file_word
                    #     print(class_name)
                    #     sensitive_file_handler.writelines(class_name)
                    #     sensitive_file_handler.write('\n')            

                    # sensitive_file_handler.close()
                except Exception as e:
                    print('');
        elif path.isdir(real_url):
            scaner_file(real_url, result_url)
        else:
            print('')

def reDel(url):
    file = os.listdir(url)
    for f in file:
        real_url = path.join(url, f)
        content = ['']
        if path.isfile(real_url):
            file_name = path.abspath(real_url)
            try:
                anversion = open(file_name, "rt")
                for line in anversion:
                    if content.__contains__(str(line)):
                        continue
                    else:
                        content.append(str(line))
                anversion.close()
                file_handler = open(file_name, 'w', encoding="utf-8")
                content.sort()
                for _line in content:
                    file_handler.writelines(_line)
                file_handler.close()
            except Exception as e:
                print(e);


def resetDir(url):
    if os.path.exists(url):
        file_list = os.listdir(url)
        for file in file_list:
            file_path = path.join(url, file)
            if path.isdir(file_path):
                resetDir(file_path)
            else:
                os.remove(file_path)
    else:
        os.makedirs(url)




if __name__ == '__main__':
    argvs = sys.argv
    real_path = argvs[1]
    resultUrl = 'codeScan/'
    resetDir(resultUrl)
    scaner_file(real_path, resultUrl)
    reDel(resultUrl)
