from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages?EAALDLMirOvEBANQZB3QtTFMlmxwuOi6XYvO06tqDgkl72xbjQptFgVoHHGWR5etfHc6ow7DwkmBrq2vNTnZCCeuWXusa852lOTc8iZAeVZAiRIZAxXgui2xouUvNV1mhClQbvG98AKrrQBZATO5tsEaeZCsKeAj5Jdot1G2DbU7ajwCr8dCPaEq'
VERIFY_TOKEN = 'hafeezkhan1806'
PAGE_ACCESS_TOKEN = 'EAALDLMirOvEBANQZB3QtTFMlmxwuOi6XYvO06tqDgkl72xbjQptFgVoHHGWR5etfHc6ow7DwkmBrq2vNTnZCCeuWXusa852lOTc8iZAeVZAiRIZAxXgui2xouUvNV1mhClQbvG98AKrrQBZATO5tsEaeZCsKeAj5Jdot1G2DbU7ajwCr8dCPaEq'


def get_bot_response(message):
 input = message
 with open("data.json", "r") as jsonFile: #open file
  data = json.load(jsonFile)
 if input in data:
  return(data[input])
 else:
  return("sorry i cant repy to that yet") 
   
 


def verify_webhook(req):
 if req.args.get("hub.verify_token") == VERIFY_TOKEN:
  return req.args.get("hub.challenge")
 else:
  return "incorrect"

def respond(sender, message):
 response = get_bot_response(message)
 send_message(sender, response)


def is_user_message(message):
 return (message.get('message') and
  message['message'].get('text') and
  not message['message'].get("is_echo"))
			


def send_message(recipient_id, text):
 with open("data.json", "r") as jsonFile: #open file
  data = json.load(jsonFile)
 if "help" in data:
  payload = {
        'message': {
            "text": "How can i help you?",
            "quick_replies":[
              {
               "content_type":"text",
               "title":"todays weather",
               "payload":"<POSTBACK_PAYLOAD>",
               "image_url":"data:image/png;base64,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"
              },{
               "content_type":"text",
               "title":"megablock",
               "payload":"<POSTBACK_PAYLOAD>",
              "image_url":"data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxAQEBUPDxASEBUQFhIYEBAQFRAVDw8PFRIWGRcVFRUYHSggGBolGxUXITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGxAQGy8lICYtLS0tLS0uLi0tLy0tLS0tLS0tLS0tLS0tLS0tLy0rLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAOEA4QMBEQACEQEDEQH/xAAcAAEAAgMBAQEAAAAAAAAAAAAAAQIFBgcEAwj/xABOEAABAwIBBQgMCggGAwAAAAABAAIDBBEFBhIhMVEHIkFhcYGR0RMVFkJSU1RyoaKx0hQXIzIzYoKTo8E1Q7KzwsPT4UVzg5Lw8SQ04v/EABsBAQADAQEBAQAAAAAAAAAAAAABAgUDBAYH/8QAMhEBAAIBAgMGBAYCAwEAAAAAAAECAwQREjFSBRQhUaHRExUyQSJCYYGRsTNxI0PwBv/aAAwDAQACEQMRAD8A7igICAgICAgICAgIIc4DWbcqG74OroRrljHK9o/NW4LeSk5KRzmP5fM4tTeUQ/eR9at8K/TP8K/HxdUfzAMWpvKIfvI+tPhX6Z/g+Pi6o/mF218J1TRnkew/mo4LeUpjLSeUx/L7teDpBB5DdV2XiYlZQkQEBAQEBAQEBAQEBAQEBAQEBAQYjGsoYaVt3Xe69g1ltfGeBdMeObztDlmyxjjeWs1WWU7/AKNrYx/ucvdTR0jn4svJ2hefpjZjJsTq5PnSycxzR6LL0V09I5VeS+qvPO3/AL9nldA92lxv5xJK6xSY5OE5InmCkO0K3BKPiQn4KdqcB8Q+CnanAfEQaQ7QnBJ8SECncNI0cYNiomkpjJD1Q19VH82WQfaLh0G65WwVnnV2rqbxytLI0uV9SzQ8NkHGLO6QuFtJSeXg9VNfkjn4tjwTKiGpJaQYnN1h1s08jl4cuGcbTwaiMvJnVxegQEBAQEBAQEBAQEBAQEEE20lBr2J4q55zIrhuq41u5OJBq+UNPpjY7huSNmoda9+ipvvLL7RybbRD4NYBqC1YiIYUzMrKUCAgICAgICCHNB1i6jZMTsYPB/5Ba3RnNNgeE6+tZ+tp+HdrdnZPx7T5Nqw/EnwnMfct4QdbeRZbbbJG8OAc03B1EILICAgICAgICAgICAgIMNlBWWAiadLtLvN4Ag8VFT5ozjrPoCDXcdfnVVvAa0ei/wDEtbRV2pDB7RvvkmPLaHwXvZYgICAgICAgICBRvzKiN21wHTo/NeXU13pP+nt0V+HJWf1/ttlXT544xq6liPpX0wCss7sLtRvm8TuEIM+gICAgICAgICAgICCCbaUGpud2WYuPCb/ZGpBkUGlTvz55H7XOtyXsPQFu6eu1Ij9HzGrvxZJn9Vl6HkEBAQEBAQEBAQfCqNrOGsFc8kbw64p2lvLH5wDhwgEchC+fmNp2fWRO8bsfVgskD26NRHKFCW1QSBzQ4d8AUF0BAQEBAQEBAQEBB5MVlzIXHisOU6EGAwxmt3Mg9c8maxzvBBPQFNY3mIVvbhrMtIpdRO0r6GkeD5TJO8vuruQgICAgICAgICD5VI3pVbcl6c22YNJnQRn6oHRo/JYOeNskvqNNbixVn9FsRZdt9h9BXJ3ZTAJc6K3gkjm1hBkkBAQEBAQEBAQEBBh8pJLMa3wiTzAf3QeSibZg49KDz47Jm07+MW6Su2njfJDzau3Dhs1enFmhbteT5m/N9FZQQEBAQEBAQEBBV4uCOJRPJMc2dyWkvCW+C4+nSsXWRtfd9H2fbfFt5Sys7btI4ivK9xk1Lvns2gEcxsfaEGfQEBAQEBAQEBAQEGt5QyZ0ob4IHSdPUg+7G2AGwIMLlXJaJrfCd7AvZo673mWf2jbbHEecsM0WFti2IfPSlSgQEBAQEBAQEBAQZDJR9nSM5COkjqWVrq8pbnZlucNjWe1njwx2ZUAbSW9Or02QbQgICAgICAgICAgINVqnZ9QfO9AQe5BrWVD7yxs2C/Sf/laWhr4TP6sftO34oj9HhWmxRAQEBAQEBAQEBAQffAn5tUB4YcPRf8l4NbXektPs622SI894bYslvsdUHNmDuNpQbYCglAQEBAQEBAQEEPNgTsQanR76Qu5T0oMig1XKNhbUB5+a5oseTWP+bVqaK0cGzE7SpPxN/OHhM7dq9/FDLikqioubNaXHYNPsVZyRC0Ypnk+7Kaod82F/O0j2rlOppH3h3ro8k/ll9m4VVn9XblLetUnWY/N1js/L0+sLjBKs8DRzjqVO+08147NyeXqt2gq9rP8Ad/ZR36n6p+W5P0/k7QVe1n+7+yd+p+p8tyfp/KpwOrHgnnHUp77TzR8tyeUfyo7CasfqweQt61aNZj81J7Py9Pq+T6SpbrhdzAn2XXSNTSfvDnbRZI/LLzvmLdD2Obygj2rpGSJ5OFsM15rNqGnhsr8UKTSX3wlpfUsLe9N3HYB/y3OvLq7xwS9uhpacsfy3FYz6J4MTbpB4kGyUT86Np2tHsQfdAQEBAQEBAQEHmxF+bE8/VPSUGvYY35x5Ag9yCk0DJBmvaHDYVatprO8K3pW8bWjd54cIp26RE3n0+1XnPkn7uVdLiryq9zGgCwAA2DQFymd+btERHJeyJTZAsgmyBZAsgiyCLIKuF9B0oPFPhUD/AJ0TeUC3sXWubJXlLhbTYrc6w+lNSRxC0bQ3bbWeUqt72vO9pdMeOmONqxs+qou8mJN3oOw+0IMvgT7wjiJHpQZBAQEBAQEBAQEGNygfaG3hOA/P8kGLw5u8vtJQetBIQWCCwQSAgkBBNkE2QLIFkEWQQQgqUEFBUoKlB8Kxt2Hp6Cg9OTT969uwg9I/sgzKAgICAgICAgIMHlK/5jfOJ9AH5oPlStswciD7BBYILBBYILBBICCbIJsgWQLIIIQVKCCgqUFSgqUFJBcEbQUHxydfaUt2t9II/ug2NAQEBAQEBAQEGt5QPvMG7AB06fzQePH8bhoIDNMTYaGMbbPkfbQ1v/NCmIRM7OeU+UWNYm8/AgII2nW2wY3idI4aTyBebU63Bpo/5J8fL7prS9+T01mFZSRtzhWCW3ewyAv6HxtvzLxY+3NJedp3j/ceHpMrzgyQ1GTLHFWktdWTNLSQ5pzAQRwEZq144ZjeOThvKvdtinls3qe6p2g3lv25HjtXVy1Damd8wjZCWB+bvSXPvaw4h0KJhasttoKyR2ISxF5LGtJazgB+T6z0qZj8KsTPFsrk9WyyS1LXvLhGd4D3u+k1dA6EtEbQVmZmXxwbEJn0M8jpHOezPzXG122jBFudTMRxQiszwzJ2wm7Wdm7I7smdbP0Z1uzW9mhNo4tjeeDdGM4hMyhglbI5r35mc4Wu68bib84SsRxSWmeGJffKCtljkpgx5aJDvwO+30evpPSorEbSm0zEww261i1RSU0L6aZ0LnzZriy13N7G820jaAq1WtLl/dtinls3qe6rbQrvJ3a4p5bN6nuptBvLa8Moco52B/wowg6R2d4a4jzWscRzrKzds6TFbh3mf9R7zDtXBkmN1K7E8ew20lQ8VEd987Q+PkJADm8pAXbS9o6fUzw0nx8p8JRfHenNvOSWVEOIxF7BmPZYSxE3LCdRB4WngK9sxsrE7shhzsyoHnEdKhLaUBAQEBAQEBAQarVuz6g+d6Ag5Zuq1T58RjpQbCNsbWjg7JMQS63O0cymbcNZtP28f4UnxnZ1PCcPjpoWQRNzWxgDlPCTtJPCvzvPmtmyTktPjLUrWKxtD2Lis5VuwYSxj4qtgDTKSyS3fOAu13LYEdC+q/8An9Ra1bYZ+3jDxaqkRMWc5X0byOm7h301V5kH7UirZardsM/Sk3mH+WrT9KsfXKMlvpqzzv45Etygpzl5sn/0dU/6n7pqm31Qiv0yn/CPtfz0/OfkRj/6OpvsfunJX6pLfRD0ZUfS0fL/ABRKK8pTfnDAbuH/AKlP/nn9y9VqvZx1WUbnuV4SyorDJIA4UzQ4NOoyONmk8lj6Fjduai2LTxWv5p2/b7vRpqRa28/Z2hfFtB86iFsjHRvaHNeCHNOkFp1gq1bTS0WrzgmN/CXHMmr0GOCnYTmmV0JHhRyaW322u08y/QtNm+Ngrkn7wyrV4bzDrE5zZg7jaV1WbYCglAQEBAQEBBDjYE7EGp0e+kLvOPT/ANoOZ7rNA+GsjrWjeyBlncDZojoB5QGnmKnaLVms/dSfCd3SMncZjrKdk8RvcDPb30b7aWuX59q9NfTZZx2/b9YaeO8XjeGTXmXch3WMdZPMyliIcILmRw0jspFs0HiF78q+u7C0lsVJy38OLl/p4dTki08MfZoS33ldN3DfpqvzIP2pFWy1W7YZ+lJvMP8AKVp+lWPrlGS301Z538UiW5QU5y8+T/6Oqf8AU/dNU2+qEV+mT/B/tfz1H5z8iMf/AEdTfY/dOU1+qS30w9GVH0tHy/xRKK8pTfnDAbuH/qU/+ef3L1Wq9nHVZRte5vjjKSs+VObHO3Mc46mOvdpPFe451ldsaS2owfg518fd3wXitvH7u3g30jTfUdoXw7RefEa6OnidNM4MYwXJPsG08S6YsV8t4pSN5lFrRWN5cjyMifiGMGqzSGse6Z58EDRG08d83oK/QsGKMOGuOPtGzLmeK0y6vibdIO0H0f8Aaus2ajfnRtdtaPYg+yAgICAgICDzYi/NiefqnpKDXcMb848gQfTFcMhqonQTsz2P1jhB4CDwEbUHO37n+IUkhkw2q0Hgc7MfbY7vXLnmw4s0cOSsSiOKv0yvW4LlJM3MfOzNOghkkTCRxljQV5sfZmjxzxVp4/rvP9ytOTJPOWB+LHE/Ah+9HUtDeHPhk+LDFPAh+9HUm8HDLdtzDJSrw+Sd1S1gErYgzMeHaWueTfZ84KJlNY2bNRYbK2ukqHAZj2kNNxe+84PslJmOHZEVni3RgWFyxSVDngATG7LEG++edOz5wU2mJ2K1mJl8sJweaOjmgeG58mdmAOBGlgAueDSEm0TO6K1mKzCe083a/wCDWb2TOvbOGbbsudr5E4o4tzhnh2VxbB5pKOGBgbnx5ucC4AaGOBseHSUi0b7lqzNYh9ccwuWV9O5gBEJ39yBbSw6NvzSlZiN02rMzDFbp2T1RXwRR0wYXRy57s9waM3sbm6DykKsSm0budfFhingQ/ejqVt4Rwyj4sMT8CH70dScUHDLNYbk9lFTNzIZmNaNTXSRvaOQPabLxZuz9LmnivTx/j+l63yV5SmbIjFq147YVTQ0HUHZwHmsaA266YNNgwf4q7f8AvNFptb6pb7k/gMFDD2GBvG97tL5HeE4/lwLvMkRs9GJN3oOw+0KEsvgb7wt4rj0oMggICAgICAgxOUlS1kTWk2Mrw1vGQ1z/AGMKmKzO8+Ss2iJiJ+7H4c3eX2kqFnqQWCCwQWCCwQWCCwQSCgm6CboIugqUEFBUoKlBUoKlBUoPhWNuw9PQg+2TNQDnxX0tzXEbGvuB6WFTtO26N432ZxQkQEBAQEBBz3dYr3RGkze9e99tuaGgehzl79Fji8WifLZna/JNJpMee7OYVM2SFkjDcPaCOdeK1ZrMxL30tFqxaHqVVkhBYILBBYILBBIQWugXQTdBF0EEoKlBBQVKCpQVKCqCsts031WN+SyDUtz/ABbs2JT6d6+KzOSN4t+04869+fDwYKx+v9s3T5/iai0/bbw/Z0teBpCAgICAgIOY7sjN9TO2iUc4LetaXZ/5mV2lH0yx+59jwYfgkps1xvCTqa8628h9vKuuu0/FX4lf3ceztVw2nFbl9nQlkNtIQSEFggsEEgoLXQTdAugXQLoIugglBUoIKCpQVKCEGnZfY8I2GliO/ePlSO8j8HlPsWloNNxT8S3KOTK7R1XDHwq855/6Yjcpae2FxwRSX9C7a7/H+7h2f/l/Z2RY7cEBAQEBAQaNuuURfRsmA+hlGdxMeC39rMXt0Ntskx5wz+0ab44t5S5Mw+hblPGHz9/C27oeSWVzXgQVTg1wsGSn5r9gceA8aydXopr+PHy8m1ou0ItEUyT4+bc1mNZIQWCCQUFgUE3QTdAugXQLoIugglBBKCpKCCgqg1jKnKtlODFCQ+XUbaWxcu08S9+l0U5PxW8I/tnazX1xRw08bf05nPK5xL3Euc43JOskrb2itdofP7ze28t+3HaMmSeoI0NayNp2lxLndGa3pWRr7eEVbfZtfG1v2dRWY1hAQEBAQEHjxigbUwSQO1StLeQkaDzGxV8d5paLQpkpF6zWfu/PlTTuhkdFILOY4tcOMFfRYrxPjHKXy+akxvE84VXd52fwTKyopgGE9lYNTH3u0fVcvHn0WPL48pe7T6/Ji8J8YbdR5d0jh8oJIjw3bnN6W6fQs6/Z2WOW0tOnamGfq3h7Bljh/lH4c/uLn3HP0+se7r8w03V6T7J7ssP8o/Dn9xO45+n1j3PmGm6vSfZPdlh/lH4c/uJ3HP0+se58w03V6T7J7s8P8o/Dn9xO45+n1j3PmGm6vSfY7s8P8o/Dn9xO45+n1j3PmGm6vSfZPdnh/lH4dR7idxz9PrHufMNN1ek+x3Z4f5R+HUe4ncc/T6x7nzDTdXpPsjuzw/yj8Oo9xO45+n1j3PmGm6vSfY7s8P8AKPw5/cTuOfp9Y9z5hpur0n2R3Z4f5R+HP7idxz9PrHufMNN1ek+yO7LD/KPw5/cTuOfp9Y9z5hpur0n2R3Y4f5R+HP7idxz9PrHufMNN1ek+zzVWXNG0bwvlPAGtLR0usr17PzTz8FL9p4I5by1XGctKicFkXyDDrzT8oR53BzL34dBjp428ZZuftLJk8K+EerWV72cq7ToGniGslcsk/Z1x1+7uuROD/BKKONws92/l/wAx3BzCw5l8/qMnxMky+m0uL4eOI+/3Z5cHoEBAQEBAQEHNd1PJon/z4W3sLVDRrtwSfkeY7Vo6LP8A9c/sy9fp/wDsr+/u5s0rYpbdh3rt4rK7mICJEQICJEQICJEQICJEQICAiUOKra2y1a7y3Pc1yZNRMKuVvyUJ3l/1s3BbiGs8duNZesz8NeGOctfQ6fitxzyj+3X1ktoQEBAQEBAQEFXsDgWuAIIsQdRB4EObkeXGRD6ZxqKVpfCdLmDS+A8nCzj4FrabVRb8NubF1Wjmk8VOX9NKa5aVb+bKtj8ll0cxARAgIkRAgIkRAgIkRAgIlUuVJvEcl645nm2fI7I6WueJJAY4Ad886HSfVZ18C8Go1UY/CPGWlpdJOTxnwq7NSUrIWNijaGNYAGtGoALGtabTvLcrWKxtD7KFhAQEBAQEBAQEEEIObbo+T+GwRmqdL8FkN82NgDhO/YI7ix4wQNq9mHWXr4T4w8GfRUv418Jcrjr4z31uXQvfTV45++zOvoskfbdf4Wzw29IXTvNOpy7pfoZCkw+eVgkije9p1OaNB5E71j6k9zyT+R9u0tX4iToCjvWPqT3LL0HaWr8RJ0BO9Y+o7ll6DtLV+Ik6AnesfUdyy9B2lq/ESdATvWPqO5Zeg7S1fiJOgJ3rH1HcsvQdpavxEnQE71j6juWXoO0tX4iToCd6x9R3LL0HaWr8RJ0BO9Y+o7ll6HznwupjaXvhe1rRdziNAG0qe9Y+o7nk6GN+GM8NvSE7zTqV7pfoVfXRjvr8mlUtqscffd0po8k/bZ1DILJChqI21Tp21er5JoLY43bHtO+JHHYcS8OXW2nwrG39tDDoK18bzv8A06XGwNAa0AAaABoAC8O+7RiNlkBAQEBAQEBAQEBBpOXe6FBh4MMVp6gjRGDvIuOQj9nWeLWpiFZnZwrGMWnrJTPUyGR7uE6mjwWjvRxK6jwoNnyOyWNW7sst2wtOngMpHeg7NpUTK0Ru6rFG1rQ1oDWtADWjQABwAKi6yAgICAgICAgEIOaZa5JdhJqaYfJnTJGP1R2j6vs5FaJUmGmKyrIYHjdRRSiamkMbhrGtjxse3UQiXdMiN0OnxACKS0FRwxk7yTjjcdfJrVJheJ3bqoSICAgICAgICCsjw0FziGhoJJJsABwkoORZfbqJN6bDXWGkSVXDyRe90bVaIUm3k5O95cS5xJJNySbknaSrKqoNjyQyYdWOz5LthYd84aDIR3rT7SomdkxG7rEELY2hjGhrWgBrRoAA4AqOi6AgICAgICAgICCHAEWIuDrB1EIOY5aZJ/ByainHyR0vYP1J4vq+xXiVJjZqClVLXEEEEgjSCNBB2goOo5C7qb4s2nxImRmplT+sZxSDvh9bXtvrVZhaLebsVNUMlYJI3Ne1wu1zSC1w4iqrvqgICAgICAgx+N4LBWx9hqWuey9yxsk0YcfrdjcM4cR0JuiY3a/8WGDeSH7+r/qKd5RwwfFhg3kh+/q/6ibycMI+K/BvJD9/V/1E4pOGGdpcnqSJjY44QxrBZrQ59gOlQs+vaan8X6z+tA7TU/i/Wf1oHaan8X6z+tA7TU/i/Wf1oHaan8X6z+tA7TU/i/Wf1oHaan8X6z+tA7TU/i/Wf1oHaan8X6z+tA7TU/i/Wf1oHaan8X6z+tA7TU/i/Wf1oIfglMQQY7gixBc8gg8BF0GvncwwbX8D17J6sDmAk0Kd5V4YPiwwbyQ/f1f9RN5OGD4sMG8kP39X/UTeThhmsAycpaBrm0jHxtfpLDLPIy+0NkeQ08YskymI2ZZQkQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEH/9k="
              }
	    ]
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }
 else:
  payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }
  
 auth = { 'access_token': PAGE_ACCESS_TOKEN }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )
 return response.json()			


@app.route("/",methods=['GET','POST'])
def listen():
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)
        return "ok"
		
if __name__ == "__main__":
 app.run()		
