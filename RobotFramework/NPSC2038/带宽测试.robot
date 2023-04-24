*** Settings ***
Documentation     测试芯片的带宽性能。
Library           BuiltIn
Library           ../../Driver/NPSC2038/NPSC2038Driver.py
Library           ../../Driver/Instrument/AgilentN9020A.py

*** Variables ***
${FREQ}           223


*** Test Cases ***
占用带宽1
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<28800 Hz
    [Tags]    FSK    9.6Kbps    带宽测试
    set_mode    FSK
    set_datarate    9.6
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 28800    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW} Hz    # 将测试结果显示在测试报告的message表格中

占用带宽2
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<57600 Hz
    [Tags]    FSK    19.2Kbps    带宽测试
    set_mode    FSK
    set_datarate    19.2
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 57600    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽3
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<115200 Hz
    [Tags]    FSK    38.4Kbps    带宽测试
    set_mode    FSK
    set_datarate    38.4
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 115200    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽4
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<230400 Hz
    [Tags]    FSK    76.8Kbps    带宽测试
    set_mode    FSK
    set_datarate    76.8
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    1
    Should Be True    ${BW} < 230400    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽5
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<460800 Hz
    [Tags]    FSK    153.6Kbps    带宽测试
    set_mode    FSK
    set_datarate    153.6
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    2
    Should Be True    ${BW} < 460800    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽6
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：不支持
    [Tags]    FSK    307.2Kbps    带宽测试
    Log    The result is 不支持    # 在日志文件中记录结果信息
    Set Test Message    不支持    # 将测试结果显示在测试报告的message表格中

占用带宽7
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<11040 Hz
    [Tags]    GFSK    9.6Kbps    带宽测试
    set_mode    GFSK
    set_datarate    9.6
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 11040    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽8
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<22080 Hz
    [Tags]    GFSK    19.2Kbps    带宽测试
    set_mode    GFSK
    set_datarate    19.2
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 22080    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽9
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<44160 Hz
    [Tags]    GFSK    38.4Kbps    带宽测试
    set_mode    GFSK
    set_datarate    38.4
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 44160    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽10
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<88320 Hz
    [Tags]    GFSK    76.8Kbps    带宽测试
    set_mode    GFSK
    set_datarate    76.8
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.5
    Should Be True    ${BW} < 88320    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽11
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<176640 Hz
    [Tags]    GFSK    153.6Kbps    带宽测试
    set_mode    GFSK
    set_datarate    153.6
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    1
    Should Be True    ${BW} < 176640    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽12
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<353280 Hz
    [Tags]    GFSK    307.2Kbps    带宽测试
    set_mode    GFSK
    set_datarate    307.2
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    2
    Should Be True    ${BW} < 353280    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽13
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<11520 Hz
    [Tags]    MSK    9.6Kbps    带宽测试
    set_mode    MSK
    set_datarate    9.6
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 11520    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽14
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<23040 Hz
    [Tags]    MSK    19.2Kbps    带宽测试
    set_mode    MSK
    set_datarate    19.2
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 23040    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽15
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<46080 Hz
    [Tags]    MSK    38.4Kbps    带宽测试
    set_mode    MSK
    set_datarate    38.4
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 46080    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽16
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<92160 Hz
    [Tags]    MSK    76.8Kbps    带宽测试
    set_mode    MSK
    set_datarate    76.8
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.5
    Should Be True    ${BW} < 92160    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽17
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<184320 Hz
    [Tags]    MSK    153.6Kbps    带宽测试
    set_mode    MSK
    set_datarate    153.6
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    1
    Should Be True    ${BW} < 184320    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽18
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<368640 Hz
    [Tags]    MSK    307.2Kbps    带宽测试
    set_mode    MSK
    set_datarate    307.2
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    2
    Should Be True    ${BW} < 368640    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽19
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<11040 Hz
    [Tags]    GMSK    9.6Kbps    带宽测试
    set_mode    GMSK
    set_datarate    9.6
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 11040    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽20
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<22080 Hz
    [Tags]    GMSK    19.2Kbps    带宽测试
    set_mode    GMSK
    set_datarate    19.2
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 22080    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽21
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<44160 Hz
    [Tags]    GMSK    38.4Kbps    带宽测试
    set_mode    GMSK
    set_datarate    38.4
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.2
    Should Be True    ${BW} < 44160    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽22
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<88320 Hz
    [Tags]    GMSK    76.8Kbps    带宽测试
    set_mode    GMSK
    set_datarate    76.8
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    0.5
    Should Be True    ${BW} < 88320    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽23
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<176640 Hz
    [Tags]    GMSK    153.6Kbps    带宽测试
    set_mode    GMSK
    set_datarate    153.6
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    1
    Should Be True    ${BW} < 176640    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中

占用带宽24
    [Documentation]    说明：测试不同速率下占用带宽
    ...    指标：<353280 Hz
    [Tags]    GMSK    307.2Kbps    带宽测试
    set_mode    GMSK
    set_datarate    307.2
    set_freq_tx    ${FREQ}
    start_tramsmit
    setCentralFreqMHz    ${FREQ}
    setReferenceLevelDBM    20
    ${BW}    getOccupiedBandWidth    2
    Should Be True    ${BW} < 353280    #单位Hz
    Log    The result is ${BW}    # 在日志文件中记录结果信息
    Set Test Message    ${BW}Hz    # 将测试结果显示在测试报告的message表格中
