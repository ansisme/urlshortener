# Architecture Diagram of URL Shortener
![Architecture Diagram](https://github.com/ansisme/urlshortener/blob/master/URL-Shortener.png)
[Architecture Diagram](https://github.com/ansisme/urlshortener/blob/master/URL-Shortener.png)

The project is build using 6 most useful Serverless services of `AWS` .
1. AWS Lambda
2. AWS API Gateway
3. AWS DynamoDB
4. AWS S3
5. AWS CLoudfront
6. AWS IAM

   
## Steps

Follow steps to make your own URL Shortener !:

1. ### Create a DynamoDB Table

Mention the primary Key as `short_id`.

2. ### Create an IAM Role

Paste the following code in the IAM Policy and attach to your IAM Role.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:UpdateItem",
                "dynamodb:Query",
                "dynamodb:GetItem"
            ],
            "Resource": "arn:aws:dynamodb:<region>:<account-id>:table/<table-name>"
        }
    ]
}

```
Replace `region`, `account-id`, `table-name` by your specifications.

Additionally, attach `AWSLambdaFullAccess` Policy too.

3. ### Create a Lambda Function
Create a basic Lambda function and attach the `IAM Role` you just created in step 2.
  - Create a Lambda Layer and choose AWS Layers, select `AWSLambdaPowertoolsPythonV2`.
  - Follow the lambda structure given in the backend code in the `backend folder`.

Add your `Invoke URL` in the Environment variables after you carete an API in the API Gateway. Along with that add your table name in the Environment Variables too under the Conguration tab of the Lambda Function.

>**Make sure you add a `/` after the Invoke URL when adding the Environment Variables.**

4. ### Create an s3 Bucket
Create an s3 bucket, enable `ACL` and grant turn off `Block public` access. 

Edit the bukcet policy as follows: 
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::Bucket-Name/*"
            ]
        }
    ]
}
```
Enable Static Hosting, verify if the URL is working.

After S3 setup, fork and clone this repo as `git clone https://github.com/<yourusername>/urlshortener`.

Run `npm install` and then `npm run build`.

Upload the `build` folder of the frontend in the S3 bucket, make sure the objects are accessible publically.

5. ### Create an API in API Gateway
Create a REST API
   - Attach the Lmabda function you created above 
   - Create two methods
     - POST under the `/create` Resource and GET in the `/{shortId}` Resource.
   - In `Integration Response` enable `Lambda Proxy Integration` for both the Methods.
   - Enable CORS for both POST and GET methods.

When you test both the methods, make sure you get status code `200` for the POST Request (after adding request body) and `301` for the GET Request (no request body required).

Finally **Deploy API** when you feel everything is working just fine, copy your `Invoke URL` and paste it in the `url.jsx` by replacing the one that's already there.

Now run `npm start` for the project to test locally on `localhost:3000` or simply visit your static website url to test the website configured with your API. Try pasting long URLs in the searchbox and shorten them, share it with your friends!

6. ### Configure AWS Cloudfront with S3

To globally host your website on a distributed network we use `AWS CDN`.
   - Click on `Create distribution` and choose Origin Domain related to S3.
   - Create OAC, AWS will itself give the name you just need to click on Create
   - Viewer and Protocol Policy `Redirect HTTP to HTTPS`
   - Cache Policy `Cache Optimized`
   - Default root object write `index.html`
   - Click on Do not enable security protections under `WAF`.

   The things I didn't mention above, leave up to default settings.

Copy the policy provided by AWS CDN, and go the `Permissions` tab of your S3 Bucket and paste it in the `Bucket Policy`. Remove the code entered earlier.

So, now if you go to check the S3 deployed static website, you will say `403 forbidden`, that's alright!

Finally go back to AWS CDN, copy the Cloudfront DNS and paste it in the browser and boom, your website is now hosted on AWS CDN globally distributed to users at a lower latency. 


