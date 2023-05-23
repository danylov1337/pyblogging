*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${LOGIN_URL}  http://localhost:8000/users/login/
${BROWSER}  Chrome
${DELAY}  5s
${USERNAME}  danylo_v
${PASSWORD}  $43Z4Km1$

*** Test Cases ***
User Can Login And See Profile After This look On Posts
    Open Browser  ${LOGIN_URL}  ${BROWSER}
    Input Text  id_username  ${USERNAME}
    Input Text  id_password  ${PASSWORD}
    Click Button  Login
    Wait Until Page Contains  ${USERNAME}'s profile
    Page Should Contain  ${USERNAME}'s profile
    Page Should Contain  View posts
    Click Link  View posts
    Wait Until Page Contains  Posts
    Page Should Contain  Posts
    [Teardown]  Close Browser

User Can Login Create Post Add Comment
    Open Browser  ${LOGIN_URL}  ${BROWSER}
    Input Text  id_username  ${USERNAME}
    Input Text  id_password  ${PASSWORD}
    Click Button  Login
    Wait Until Page Contains  ${USERNAME}'s profile
    Page Should Contain  ${USERNAME}'s profile
    Page Should Contain  Create post
    Click Link  Create post
    Input Text  id_title  LoremIpsum54
    Input Text  id_content  DolorSitAmet
    Click Button  Save
    Wait Until Page Contains  LoremIpsum54
    Page Should Contain  LoremIpsum54
    Click Link  Add comment
    Input Text  id_content  Good point from your side
    Click Button  Save
    Wait Until Page Contains  Good point from your side
    [Teardown]  Close Browser

*** Keywords ***
Login
    [Arguments]  ${username}  ${password}
    Input Text  id_username  ${username}
    Input Text  id_password  ${password}
    Click Button  Login

*** Keywords ***
Validate Post
    [Arguments]  ${post_content}
    Page Should Contain  ${post_content}
