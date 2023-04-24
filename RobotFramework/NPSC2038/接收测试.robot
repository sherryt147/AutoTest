*** Settings ***
Documentation     测试芯片的接收灵敏度
Library           BuiltIn
Library           ../../Driver/NPSC2038/NPSC2038Driver.py
Library           ../../Driver/Instrument/KeysightSMBV100A.py

*** Variables ***
${FREQ}           223
${SENSITIVITY}    -80

*** Test Cases ***
接收灵敏度1
    [Documentation]    测试指标：在设定功率下，达成95%的数据准确率
    [Tags]    ${FREQ}MHz    FSK    9.6Kbps    RX
    preConfiguration    ${SENSITIVITY}    ${FREQ}
    chip_reset
    set_freq_rx    ${FREQ}
    start_receive
    executeTrigger
    delay_ms    500
    ${Result}    receive_done
    Set Test Message    数据完整率${Result}%    # 将测试结果显示在测试报告的message表格中
    Should be TRUE ${Result}>95
    Log    The result is ${Result}    # 在日志文件中记录结果信息

