import requests
import time,json


#  Request to initiate Auth for getting Session Token

targetPhone = ""               
url = "https://cognito-idp.eu-central-1.amazonaws.com"
countforSecondRequestTries = 0
checkResponseReqTwo = True
response1 = ''
response2 = ''
TotalNoofRequests = 0
TotalAuthReq = 0
TotalOtpReq = 0
SuccessRequests = 0
AuthSuccessRequest = 0
AuthFailedRequest = 0
OtpSuccessRequest = 0
OtpFailedRequest = 0
FailedRequest = 0

SleepParam = 0
TotalUsers = []


print("length of Total users : " , len(TotalUsers))
print(type(TotalUsers))
TriesPerUser = [0] * len(TotalUsers)


print("Length of TotalUser : ",len(TotalUsers))
print("Length of Triesuserlist : ",len(TriesPerUser))
with open("ReportsResult.txt" , "w") as Report, open("RequestBody.txt", "w" ,encoding="utf-8") as body,open("TriesPerUser.txt" , "w") as tries:
    for i in range(len(TotalUsers)):      # we can pass a list of numbers to iterate through it
        targetPhone = TotalUsers[i]
        print("targetPhone" , targetPhone)
        #print(type(targetPhone))
        print("Value for i " , i)
        #print("Value of TriesPerUser[i] ", TriesPerUser[i  - 1])
        #TriesPerUser[i] = 0
        checkResponseReqTwo = True
        while(checkResponseReqTwo != False):     # This will keep sending requests with a single phone number until it will recieve a 400
            TriesPerUser[i - 1] = TriesPerUser[i - 1] + 1
            TotalNoofRequests = TotalNoofRequests + 1
            headers1 = {"Aws-Sdk-Invocation-Id": "Your SDK Invocation ID Here",
                        "User-Agent": "User Agent you want to use",
                        "Aws-Sdk-Retry": "0/0",
                        "Accept-Encoding": "gzip, deflate",
                        "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
                        "Content-Type": "application/x-amz-json-1.1",
                        "Content-Length": "2184"}
            
            data = {"AuthFlow":"CUSTOM_AUTH",
                    "AuthParameters":{"USERNAME":" UserName Here",
                    "SRP_A":"Youur SRP_A Here"}}
            data['AuthParameters']['USERNAME'] = targetPhone
            print("********* Session Token Request  ************")
            #print(data)
            #break    # for testing purpose
            start = time.perf_counter()
            response1 = requests.post(url,headers=headers1, json=data)
            request_time = time.perf_counter() - start
            #print(type(request_time))
            RespTime = request_time
            #print(str(RespTime))
            # Report Writing in File
            Report.write("InitiateAuth Request")
            Report.write('\n')
            Report.write('Request No : ')
            Report.write(str(i+1))
            Report.write('\n')
            Report.write(TotalUsers[i])
            Report.write('\n')
            Report.write('Response Code : ')
            Report.write(str(response1.status_code))
            Report.write('\n')
            Report.write('Reponse time:')
            Report.write(str(RespTime))
            Report.write('\n')
            
            #   Writing Reports in file     -       Response Body
            body.write("InitiateAuth Request")
            body.write('\n')
            body.write('Request No : ')
            body.write(str(i+1))
            body.write('\n')
            body.write('Response body : \n')
            body.writelines(response1.text)
            #body.write(json.dumps(response1, ensure_ascii=False))
            body.write('\n')
            
            
            
            print("Request completed in {0:.0f}ms".format(request_time))
            #self.logger.info("Request completed in {0:.0f}ms".format(request_time))
            print("Status Code", response1.status_code)
            #print("JSON Response ", response1.json())       # Request response data
            print("************  Session Token Request End   *********")
            if response1.status_code == 200:
                AuthSuccessRequest = AuthSuccessRequest + 1
                print("********** OTP Request Start **********")
                print("OTP Request True")
                JsonResponse = response1.json()
                SessionToken = JsonResponse['Session']
                #print("Session Token : ",SessionToken)
                challengeParams = JsonResponse['ChallengeParameters']
                UserName = challengeParams['USERNAME']
                #      Request to RespondToAuthChallenge

                headers2 = {"Aws-Sdk-Invocation-Id": "Your AWS Invocation Id here",
                            "User-Agent": "User agent to use",
                            "Aws-Sdk-Retry": "0/0",
                            "Accept-Encoding": "gzip, deflate",
                            "X-Amz-Target": "AWSCognitoIdentityProviderService.RespondToAuthChallenge",
                            "Content-Type": "application/x-amz-json-1.1",
                            "Content-Length": "1330"}
                            
                data2 = {
                " Body for request"
                
                }
                data2['ClientMetadata']['username'] = targetPhone
                data2['Session'] = SessionToken
                data2['ChallengeResponses']['USERNAME'] = UserName
                #print(data2)
                
                start = time.perf_counter()
                response2 = requests.post(url,headers=headers2, json=data2)
                request_time = time.perf_counter() - start
                RespTime2 = request_time
                #   Writing Reports in file     -       ResponseCode + time
                Report.write("Sending OTP Request")
                Report.write('\n')
                Report.write('Request No : ')
                Report.write(str(i+1))
                Report.write('\n')
                Report.write('Response Code : ')
                Report.write(str(response1.status_code))
                Report.write('\n')
                Report.write('Reponse time: ')
                Report.write(str(RespTime2))
                Report.write('\n')
                
                #   Writing Reports in file     -       Response Body
                body.write("Sending OTP Request")
                body.write('\n')
                body.write('Request No : ')
                body.write(str(i+1))
                body.write('\n')
                body.write('Response body : \n')
                body.writelines(response2.text)
                #body.write(json.dumps(response2, ensure_ascii=False))
                body.write('\n')
                

                #print("Request completed in {0:.0f}ms".format(request_time))
                print("Status Code", response2.status_code)
                #print("JSON Response ", response2.json())       # Request response data
                print("********** OTP Request End ***********")
                if response2.status_code == 200:
                    OtpSuccessRequest = OtpSuccessRequest + 1
                    checkResponseReqTwo = True
                    countforSecondRequestTries = countforSecondRequestTries + 1
                else:
                    print("Response of OTP request threw code other than 200")
                    OtpFailedRequest = + 1
            else:
                #print("JSON Response ", response2.json())
                AuthFailedRequest = AuthFailedRequest + 1
                checkResponseReqTwo = False
        tries.write("Tries of User No. ")
        tries.write(str(i+1))
        tries.write("  are : ")
        tries.write(str(TriesPerUser[i - 1]))
        tries.write('\n')
tries.close()
print("No of tries that went success 200 with Session Token : ", countforSecondRequestTries)
print("Total requests Made : " , TotalNoofRequests)
print("Total Request Made for Initiate Auth : ", TotalNoofRequests)
print("Success Requests made for Initiate Auth : " , AuthSuccessRequest)
print("Total Request Made for Send OTP : " , AuthSuccessRequest)
print("Success Requests made for Send OTP      : " , OtpSuccessRequest)

   

with open("TotalRequest.txt" , "w") as ReqResult:
    ReqResult.write("Total requests Made : ")
    ReqResult.write(str(TotalNoofRequests))
    ReqResult.write("\n")
    ReqResult.write("Total Request Made for Initiate Auth : ")
    ReqResult.write(str(TotalNoofRequests))  # bcz this is the first req so total no of Auth will be same of Totalrequests 
    ReqResult.write("\n")
    ReqResult.write("Success Requests made for Initiate Auth : ")
    ReqResult.write(str(AuthSuccessRequest))
    ReqResult.write("\n")
    ReqResult.write("Total Request Made for Send OTP : ")
    ReqResult.write(str(AuthSuccessRequest))  # Bcz whenever the auth request will be successful the otp req will be initiated so Auth success = total OTP req
    ReqResult.write("\n")
    ReqResult.write("Success Requests made for Send OTP      : ")
    ReqResult.write(str(OtpSuccessRequest))

  
Report.close()
body.close()
ReqResult.close()  
print("No of tries that went success 200 with Session Token : ", countforSecondRequestTries)
countforSecondRequestTries = 0

