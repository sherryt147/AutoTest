*** Settings ***
Documentation     测试芯片的射频相关性能。123
Library           BuiltIn

*** Variables ***
${FREQ}           470
${RF_LOSS}        0.5



*** Test Cases ***
发射功率Min
    [Documentation]    说明：测试发射功率最小值
    ...    指标：-40dBm±1dBm
    [Tags]    TX    发射功率    ${FREQ}MHz
    Should Be True    1000>${FREQ} > 0
    Log    The result is ${FREQ}    # 在日志文件中记录结果信息
    Set Test Message    ${FREQ}dBm    # 将测试结果显示在测试报告的message表格中

发射功率2
    [Documentation]    说明：测试发射功率最小值
    ...    指标：-40dBm±1dBm
    [Tags]    TX    发射功率    ${FREQ}MHz
    Should Be True    100<${FREQ} < 500
    Log    The result is ${FREQ}    # 在日志文件中记录结果信息
    Set Test Message    ${FREQ}dBm    # 将测试结果显示在测试报告的message表格中
发射功率3
    [Documentation]    说明：测试发射功率最小值
    ...    指标：-40dBm±1dBm
    [Tags]    TX    发射功率    ${FREQ}MHz
    Should Be True    100<${FREQ} < 200
    Log    The result is ${FREQ}    # 在日志文件中记录结果信息
    Set Test Message    ${FREQ}dBm    # 将测试结果显示在测试报告的message表格中
发射功率4
    [Documentation]    说明：测试发射功率最小值
    ...    指标：-40dBm±1dBm
    [Tags]    TX    发射功率    ${FREQ}MHz
    Should Be True    100<${FREQ} < 200
    Log    The result is ${FREQ}    # 在日志文件中记录结果信息
    Set Test Message    ${FREQ}dBm    # 将测试结果显示在测试报告的message表格中
    
    
    
    
