'use strict'
const AWS = require('aws-sdk');
const documentClient = new AWS.DynamoDB.DocumentClient({
   region: "ap-south-1"
});
const ses = new AWS.SES({
   region: 'ap-south-1'
});

exports.handler = async (event, context, callback) => {
   const timeLimit = 5;
   const date = new Date().toLocaleString().slice(-24).replace(/\D/g,'')

   const params = {
      TableName: "sensor_db",
      Limit: timeLimit //Time Limit
   }

   try {
      const data = await documentClient.scan(params).promise();
      let sum = 0;
      data.Items.forEach(function(item) {
         sum = sum + item.Humidity;
      });

      const avg = sum / timeLimit;

      //Trigger for Email
      if(avg <= 80) {
         //Email Body
         var eParams = {
            Destination: {
               ToAddresses: ["kushwahaankit56@gmail.com"]
            },
            Message: {
               Body: {
                  Text: {
                     Data: "Average humidity BELOW PAR, Average Humidity of last " + timeLimit + " minutes " + "is " + avg
               }
            },
            Subject: {
                  Data: "Data retrieved from sensor"
               }
            },
            Source: "cmsniperline@gmail.com"
         };

         var email = await ses.sendEmail(eParams, function(err, data) {
            if (err) {
               console.log(err);
            }
            else {
               console.log("===EMAIL SENT===");
            }
         }).promise();
      }
   } catch (err) {
      console.log(err);
   }
};