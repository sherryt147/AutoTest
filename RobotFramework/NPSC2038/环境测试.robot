*** Settings ***
Documentation     测试芯片的接收灵敏度
Library           BuiltIn

*** Variables ***
${FREQ}           23



*** Test Cases ***
接收灵敏度1
    [Documentation]    测试指标：在设定功率下，达成95%的数据准确率
    [Tags]    ${FREQ}MHz    MSK    19.6Kbps
    Set Test Message    数据完整率${FREQ}%    # 将测试结果显示在测试报告的message表格中
    IF    ${FREQ}<95
        Should Be True    ${FREQ}>95
    END
    Log    The result is ${FREQ}    # 在日志文件中记录结果信息

接收灵敏度2
    [Documentation]    测试指标：在设定功率下，达成95%的数据准确率
    [Tags]    ${FREQ}MHz    MSK    9.6Kbps
    Set Test Message    数据完整率${FREQ}%    # 将测试结果显示在测试报告的message表格中
    IF    ${FREQ}<95
        Should Be True    ${FREQ}>95
    END
    Log    The result is ${FREQ}    # 在日志文件中记录结果信息

接收灵敏度3
    [Documentation]    测试指标：在设定功率下，达成95%的数据准确率
    [Tags]    ${FREQ}MHz    FSK    19.6Kbps
    Set Test Message    数据完整率${FREQ}%    # 将测试结果显示在测试报告的message表格中
    IF    ${FREQ}<95
        Should Be True    ${FREQ}>95
    END
    Log    The result is ${FREQ}    # 在日志文件中记录结果信息

接收灵敏度4
    [Documentation]    测试指标：在设定功率下，达成95%的数据准确率
    [Tags]    ${FREQ}MHz    FSK    9.6Kbps
    Set Test Message    数据完整率${FREQ}%    # 将测试结果显示在测试报告的message表格中
    IF    ${FREQ}<95
        Should Be True    ${FREQ}>95
    END
    Log    The result is ${FREQ}    # 在日志文件中记录结果信息
