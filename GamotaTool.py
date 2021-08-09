import os
import time
import zipfile
import plistlib
import argparse
import xml.etree.ElementTree as ET
import pathlib
import shutil
from pathlib import Path


# ----------------------------------------------------------Android------------------------------------------------------------
# Decompiling APK
def decompile_apk(input):
    print('\n                  START DECODING APK')
    print('                          ↓')
    print('                          ↓')
    print('                          ↓')

    output = 'out'
    ResultFile = os.system(
        'java -jar ' + "./tools/apktool.jar" + ' d -f ' + input + " -o " + output)
    if ResultFile == 0:
        print("==============>>>> DECODING SUCCESS ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓")
        print("                          ↓")
        print("                          ↓")
        print("                          ↓")
    else:
        print("==============>>>> DECODING FAIL ✘ ✘ ✘ ✘ ✘ ✘ ✘ ✘ \n")


# Change apktool.yml extension file to apktool.txt to read version info
def change_extention():
    p = Path('./out/apktool.yml')
    p.rename(p.with_suffix('.txt'))


# Split
def split_version_value(input):
    temp = input.strip().split(":")
    tmp_0 = temp[0]
    tmp_1 = temp[1]
    result = tmp_1.replace("'", "")
    return result


# Read Version APK
def read_version_info():
    with open("./out/apktool.txt", "r") as myfile:
        data = myfile.readlines()
        version = "\n-----------------------Version------------------------------------------------"
        for line in data:
            if("minSdkVersion:" in line):
                version += "\nMin SDK Version" + \
                    "           :" + split_version_value(line)
            elif("targetSdkVersion:" in line):
                version += "\nTarget SDK Version" + \
                    "        :" + split_version_value(line)
            elif("version:" in line):
                version += "\nVersion" + "                   :" + \
                    split_version_value(line)
            elif("versionCode:" in line):
                version += "\nVersion Code" + \
                    "              :" + split_version_value(line)
            elif("versionName:" in line):
                version += "\nVersion Name" + \
                    "              :" + split_version_value(line)
        print(version)


#  Read Strings Manifest
def read_strings(value):
    m_tree = ET.parse('out/res/values/strings.xml')
    m_root = m_tree.getroot()

    for m_resources in m_root.iter('resources'):
        for m_string in m_resources.iter('string'):
            string_name = m_string.get('name')
            if(string_name in value):
                result = m_string.text
    return result

#  Read Integers Manifest


def read_integers(value):
    m_tree = ET.parse('out/res/values/integers.xml')
    m_root = m_tree.getroot()

    result = "null"
    for m_resources in m_root.iter('resources'):
        for m_integer in m_resources.iter('integer'):
            string_name = m_integer.get('name')
            if(string_name in value):
                result = m_integer.text
    return result


def handle_print(tag, value):
    if('@integer' in value):
        temp = read_integers(value)
        print(tag + ": " + temp)
    elif('@string' in value):
        temp = read_strings(value)
        print(tag + ": " + temp)
    else:
        print(tag + ": " + value)


# Read Manifest
def read_manifest_file():
    namespace = '{http://schemas.android.com/apk/res/android}'
    tree = ET.parse('out/AndroidManifest.xml')
    root = tree.getroot()
    packageName = root.attrib['package']

    for application in root.iter('application'):
        print("\n------------------Information Manifest----------------------------------------")

        # Activity
        for activity in application.iter('activity'):
            activityName = activity.get(namespace + 'name')
            # add package name
            if activityName[0] == '.':
                activityName = packageName + activityName

            # print(activityName)
            # if('FacebookActivity' in activityName):
            #     print("Login Facebook:          yes")
            # elif('SignInHubActivity' in activityName):
            #     print("Login Google:            yes")

        # Receiver
        for receiver in application.iter('receiver'):
            receiverName = receiver.get(namespace + 'name')
            if receiverName[0] == '.':
                receiverName = packageName + receiverName
            # print(receiverName)

        # meta-data
        for meta_data in application.iter('meta-data'):
            metaName = meta_data.get(namespace + 'name')
            m_value = meta_data.get(namespace + 'value')

            if metaName[0] == '.':
                metaName = packageName + metaName

            if('com.gmo.apiKey' in metaName):
                handle_print("GMO API KEY               ", m_value)
            elif('com.countly.appKey' in metaName):
                handle_print("Crashlytics App KEY       ", m_value)
            elif('com.gmo.appsflyerKey' in metaName):
                handle_print("Appflyer API KEY          ", m_value)
            elif('com.gmo.refCode' in metaName):
                handle_print("RefCode                   ", m_value)
            elif('com.facebook.sdk.ApplicationId' in metaName):
                handle_print("Facebook Application ID   ", m_value)
            elif('com.google.android.gms.version' in metaName):
                handle_print("Google Advertising        ", m_value)
            elif('com.gmo.hms.pubkey' in metaName):
                handle_print("Pubkey                    ", m_value)


# ----------------------------------------------------------IOS------------------------------------------------------------

#Rename IPA to RAR
def change_extention_ios(value):
    p = Path(value)
    p.rename(p.with_suffix('.rar'))

bar = [
    "                       ",
    "=>                     ",
    "==>                    ",
    "===>                   ",
    "====>                  ",
    "=====>                 ",
    "======>                ",
    "=======>               ",
    "========>              ",
    "=========>             ",
    "==========>            ",
    "===========>           ",
    "============>          ",
    "=============>         ",
    "==============>        ",
    "===============>       ",
    "================>      ",
    "=================>     ",
    "==================>    ",
    "===================>   ",
    "====================>  ",
    "=====================> ",
    "======================>",
    " =====================>",
    "  ====================>",
    "   ===================>",
    "    ==================>",
    "     =================>",
    "      ================>",
    "       ===============>",
    "        ==============>",
    "         =============>",
    "          ============>",
    "           ===========>",
    "            ==========>",
    "             =========>",
    "              ========>",
    "               =======>",
    "                ======>",
    "                 =====>",
    "                  ====>",
    "                   ===>",
    "                    ==>",
    "                     =>",
    "                       ",
    "                       ",
    "                       "
]

#Unzip file RAR
def unzip(value):
    temp = value.split(".")
    tmp_0 = temp[0] + ".rar"

    # zf = zipfile.ZipFile(tmp_0)
    # uncompress_size = sum((file.file_size for file in zf.infolist()))
    # extracted_size = 0
    # i = 0
    # for file in zf.infolist():
    #     extracted_size += file.file_size
    #     percentage = extracted_size * 100/uncompress_size
    #     zf.extract(file)

    #     # progress
    #     print(bar[i % len(bar)], end="\r")
    #     time.sleep(.0000000000000001)
    #     i += 1
    with zipfile.ZipFile(tmp_0, 'r') as zip_ref:
        zip_ref.extractall('./')



#Handle function print
def handle_print_ios(name, value):
    size_name = len(name)
    kq = 33 - size_name
    print(name + " " * kq + ": " + value)

#Get path Info.plist in Folder Payload
def get_path_info_plist(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for item in subfolders:
        result = item + '\Info.plist'
        return result

#Read file info.plist in Folder Payload
def read_file_plist():
    print("\n--------------------------INFORMATION IOS--------------------------")
    with open(get_path_info_plist(".\payload"), 'rb') as fp:
        pl = plistlib.load(fp)
        for d in pl:
            if "CFBundleURLTypes" in d:
                CFBundleURLTypes = pl['CFBundleURLTypes']
                for itemType in CFBundleURLTypes:
                    if "CFBundleURLName" in itemType:
                        name = itemType['CFBundleURLName']
                        schemes = itemType['CFBundleURLSchemes']
                        for item_schemes in schemes:
                            handle_print_ios(name, item_schemes)
            if "DTPlatformVersion" in d:
                handle_print_ios("DT Platform Version", pl['DTPlatformVersion'])
            elif "DTSDKBuild" in d:
                handle_print_ios("DT SDK Build", pl['DTSDKBuild'])
            elif "ADMID" in d:
                handle_print_ios("ADMID", pl['ADMID'])
            elif "CFBundleDisplayName" in d:
                handle_print_ios("CF Bundle DisplayName", pl['CFBundleDisplayName'])
            elif "CFBundleIdentifier" in d:
                handle_print_ios("CF Bundle Identifier", pl['CFBundleIdentifier'])
            elif "GMOAFKey" in d:
                handle_print_ios("GMO AF Key", pl['GMOAFKey'])
            elif "GMOAFAppID" in d:
                handle_print_ios("GMO AF App ID", pl['GMOAFAppID'])
            elif "GOOGLE_CLIENT_ID" in d:
                handle_print_ios("Google Client ID", pl['GOOGLE_CLIENT_ID'])
            elif "MinimumOSVersion" in d:
                handle_print_ios("Minimum OS Version", pl['MinimumOSVersion'])
            elif "GMOAPIKey" in d:
                handle_print_ios("GMO API Key", pl['GMOAPIKey'])
            elif "FacebookAppID" in d:
                handle_print_ios("Facebook App ID", pl['FacebookAppID'])
            elif "FacebookAppLinkUrl" in d:
                handle_print_ios("Facebook App Link Url", pl['FacebookAppLinkUrl'])
            elif "YayaAppID" in d:
                handle_print_ios("Yaya App ID", pl['YayaAppID'])
            elif "BuglyAppID" in d:
                handle_print_ios("Bugly App ID", pl['BuglyAppID'])
            elif "gameID" in d:
                handle_print_ios("Game ID", pl['gameID'])

#Delete All in folder payload
def delete_folder_payload(dirname):
    print('\n                 START DECODING IPA, PLEASE WAIT!')
    print('                                 ↓')
    print('                                 ↓')
    print('                                 ↓')

    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for item in subfolders:
        path = pathlib.Path(item)  
        shutil.rmtree(path)
# ----------------------------------------------------------END IOS------------------------------------------------------------


# handle tyoe: APK OR IPA
def handle_type(value):
    try:
        temp = value.split(".")
        extension_file = temp[len(temp) - 1]

        if(extension_file == "apk"):
            decompile_apk(value)
            change_extention()
            read_version_info()
            read_manifest_file()
        elif(extension_file == "ipa"):
            delete_folder_payload(".\Payload")
            change_extention_ios(value)
            unzip(value)
            read_file_plist()
        else:
            print("Not an APK or IPA file. Please check again !!")
    except:
        print("")


def check_exits(value):
    if not os.path.exists(value):
        return True
    return False


# Get param from CMD
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ai", "--apk-ipa", help="Apk File Or Ipa File", required=True)
    return parser.parse_args()


# Main
def main():
    args = get_args()

    if check_exits(args.apk_ipa):
        print("File does not exist. Please check again!")
        return

    handle_type(args.apk_ipa)

if __name__ == "__main__":
    main()
