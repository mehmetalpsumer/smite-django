import random, requests, base64, json

from io import BytesIO, StringIO
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.utils.text import slugify
from django.core import serializers
from PIL import Image


from smite_wrapper import Client
from .models import God, Ability, Item, ItemDescription, ItemStat

# Credentials
dev_id = "2401"
auth_key = "your_password"
client = Client(dev_id, auth_key)


# Route: /
def home(request):
    #update_gods()
    #update_items()
    return render(request, 'smite/home.html', context={'gods': God.objects.all()})


# Route: /god/list
def god_list(request):
    gods = God.objects.all().order_by('name')
    context = {
        'gods': gods
    }
    return render(request, 'smite/list_gods.html', context=context)


# Route: /god/<god>
def god(request, god_name):
    god_name = slugify(god_name)
    god = get_object_or_404(God, slug=god_name)
    lore = god.lore.replace('\\n\\n', '')
    context = {
        'id': god.id,
        'name': god.name,
        'title': god.title,
        'lore': lore,
        'abilities': [god.ability_1.get_dict(),
                      god.ability_2.get_dict(),
                      god.ability_3.get_dict(),
                      god.ability_4.get_dict(),
                      god.ability_passive.get_dict()],
        'card': god.icon_url,
    }
    return render(request, 'smite/god.html', context=context)


# Route: /random/god
def random_god(request):
    gods = God.objects.all()
    god = random.choice(gods)
    context = {
        'god': god
    }
    return render(request, 'smite/random_god.html', context=context)


# Route: /random/create_god
def create_god(request):
    context = {}
    return render(request, 'smite/create_god.html', context=context)


# JSON RESPONSES
# Route: /api/god
def god_api(request, god_name):
    if request.method == 'POST':
        god = get_object_or_404(God, slug=request.GET.get('search'))
    god = get_object_or_404(God, slug=god_name)
    lore = god.lore.replace('\\n\\n', '')
    data = {
        'id': god.id,
        'name': god.name,
        'title': god.title,
        'lore': lore,
        'ability_1': god.ability_1.get_dict(),
        'ability_2': god.ability_2.get_dict(),
        'ability_3': god.ability_3.get_dict(),
        'ability_4': god.ability_4.get_dict(),
        'ability_p': god.ability_passive.get_dict(),
        'card': god.icon_url,
    }
    return JsonResponse(data)


# Route: /api/gods
def gods_api(request):
    god_objects = God.objects.all()
    gods = []
    data = serializers.serialize('json', God.objects.all(), fields=('id', 'name'))
    for god in god_objects:
        god_dict = {
            'id': god.id,
            'slug': god.slug,
            'name': god.name,
            'title': god.title,
            'lore': god.lore.replace('\\n\\n', ''),
            'ability_1': god.ability_1.get_dict(),
            'ability_2': god.ability_2.get_dict(),
            'ability_3': god.ability_3.get_dict(),
            'ability_4': god.ability_4.get_dict(),
            'ability_p': god.ability_passive.get_dict(),
            'card': god.icon_url,
        }
        gods.append(god_dict)
    gods_serialized = json.dumps(gods)
    return JsonResponse(data)


# Route: /api/create_god
def create_god_api(request):
    gods = random.sample(list(God.objects.all()), 9)

    # Gather images to blend
    images = []
    for god in gods:
        images.append(Image.open(BytesIO(requests.get(god.icon_url).content)).convert('RGB'))
    new_image = Image.blend(images[0], images[1], 0.3)
    new_image = Image.blend(new_image, images[2], 0.3)
    buffer = BytesIO()
    new_image.save(buffer, 'PNG')
    img_str = str(base64.b64encode(buffer.getvalue()))[2:-1]

    # Generate new name
    word_size = random.randint(1, 3)
    new_name = ""
    for word in range(word_size):
        begin_word_rand = gods[random.randint(0, len(gods)-1)].name.split(' ', 1)[0]
        end_word_rand = gods[random.randint(0, len(gods)-1)].name.split(' ', 1)[0]

        if len(begin_word_rand) <= 2:
            new_name += begin_word_rand
        else:
            new_name += begin_word_rand[0:random.randint(1, len(begin_word_rand)-2)]

        if len(end_word_rand) <= 2:
            new_name += end_word_rand
        else:
            new_name += end_word_rand[random.randint(1, len(end_word_rand)-1):len(end_word_rand)]
        new_name += " "

    if new_name[len(new_name)-1] is 'the':
        print(new_name)
        new_name = new_name[:len(new_name)-2]
        print(new_name)
    new_name = new_name.title()

    # Generate skills
    abilities = [None, None, None, None, None]
    for i in range(5):
        god = random.choice(gods)
        skill = ""
        if i == 0:
            skill = god.ability_1
        elif i == 1:
            skill = god.ability_2
        elif i == 2:
            skill = god.ability_3
        elif i == 3:
            skill = god.ability_4
        elif i == 4:
            skill = god.ability_passive

        new_skill = {
            'name': str(skill.name).replace(god.name, new_name),
            'img': skill.icon_url,
            'desc': str(skill.description).replace(god.name, new_name)
        }

        abilities[i] = new_skill

    # Generate title
    title = ""
    for i in range(4):
        if gods[i].title[:3] != "The":
            title += "{} ".format(gods[i].title.split(' ')[0])
        else:
            i -= 1
        if random.randint(0, 5) > 4 and len(title)>0:
            break
    print(title)
    # Generate others
    pantheon = random.choice(gods).pantheon
    role = random.choice(gods).role
    type = random.choice(gods).type

    data = {
        'name': new_name,
        'title': title,
        'pantheon': pantheon,
        'role': role,
        'type': type,
        'abilities': abilities,
        'img_str': img_str,
    }
    return JsonResponse(data)


# Route: /api/random_god
def random_god_api(request):
    gods = God.objects.all()
    god = random.choice(gods)
    lore = god.lore.replace('\\n\\n', '')
    data = {
        'id': god.id,
        'name': god.name,
        'title': god.title,
        'lore': lore,
        'ability_1': god.ability_1.get_dict(),
        'ability_2': god.ability_2.get_dict(),
        'ability_3': god.ability_3.get_dict(),
        'ability_4': god.ability_4.get_dict(),
        'ability_p': god.ability_passive.get_dict(),
        'card': god.icon_url,
    }
    return JsonResponse(data)


# Route: /api/god_auto_complete
def god_auto_complete_api(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        gods = God.objects.filter(name__icontains=query)
        results = []
        for god in gods:
            god_json = {}
            god_json['name'] = god.name
            god_json['url'] = god.slug
            results.append(god_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


# MISC
# Updates db for items
def update_items():
    items_list = client.loop.run_until_complete(client.get_items())
    for list_item in items_list:
        item_name = list_item['DeviceName']
        print("Looking for {}".format(item_name))

        try:
            item = Item.objects.get(name=item_name)
            item.delete()
            print("{} found in DB and deleted!".format(item_name))
        except Item.DoesNotExist:
            pass

        #create
        item = Item(
            id=list_item['ItemId'],
            name=list_item['DeviceName'],
            tier=list_item['ItemTier'],
            price=list_item['Price'],
            root_item_id=list_item['RootItemId'],
            short_description=list_item['ShortDesc'],
            description=list_item['ItemDescription']['Description'],
            starting_item=False,
            type=list_item['Type'],
            icon_id=list_item['IconId'],
            icon_url=list_item['itemIcon_URL']
        )

        starter = list_item['StartingItem']
        if (starter is True) or (starter == 'true'):
            item.starting_item = True
        item.save()

        print("{} is not found, and created".format(item_name))

        stats_list = list_item['ItemDescription']['Menuitems']
        aura_desc = list_item['ItemDescription']['SecondaryDescription']

        # Create item aura object, if it is null but exist in DB, then delete it
        if (aura_desc is not None) and (aura_desc != ''):
            try:
                aura = ItemDescription.objects.get(item_id=item.id)
                aura.aura = aura_desc
                aura.save()
                print("Aura is found and updated!")
            except ItemDescription.DoesNotExist:
                aura = ItemDescription(
                    item_id=item.id,
                    aura=aura_desc
                )
                aura.save()
                print("New aura is created")
        else:
            try:
                aura = ItemDescription.objects.get(item_id=item.id)
                aura.delete()
                print("Aura change detected, deleted.")
            except ItemDescription.DoesNotExist:
                pass

        # Delete all related stats
        for stat in ItemStat.objects.filter(item_id=item.id):
            stat.delete()
        for stat in stats_list:
            stat_obj = ItemStat(
                item_id=item.id,
                stat=stat['Description'],
                value=stat['Value']
            )
            stat_obj.save()


# Updates db for gods
def update_gods():
    gods_list = client.loop.run_until_complete(client.get_characters())
    print('Total number of gods: {}'.format(God.objects.all().count()))
    for god in gods_list:
        abilities = []
        for i in range(1, 6):
            ability = Ability(
                id=god['AbilityId' + str(i)],
                name=god['Ability' + str(i)],
                icon_url=god['Ability_' + str(i)]['URL'],
                description=god['Ability_' + str(i)]['Description']['itemDescription']['description']
            )
            abilities.append(ability)
            print('Adding ability {} for {}...'.format(ability.name, god['Name']))
            ability.save()
        god_new = God(
            id=god['id'],
            name=god['Name'],
            lore=god['Lore'],
            pantheon=god['Pantheon'],
            role=god['Roles'],
            title=god['Title'],
            type=god['Type'],
            card_url=god['godCard_URL'],
            icon_url=god['godIcon_URL'],
            latest_god=False,
            hp=god['Health'],
            mp=god['Mana'],
            hp5=god['HealthPerFive'],
            mp5=god['ManaPerFive'],
            hp_pl=god['HealthPerLevel'],
            mp_pl=god['ManaPerLevel'],
            hp5_pl=god['HP5PerLevel'],
            mp5_pl=god['MP5PerLevel'],
            speed=god['Speed'],
            mag_protection=god['MagicProtection'],
            mag_protection_pl=god['MagicProtectionPerLevel'],
            phy_protection=god['PhysicalProtection'],
            phy_protection_pl=god['PhysicalProtectionPerLevel'],
            mag_power=god['MagicalPower'],
            mag_power_pl=god['MagicalPowerPerLevel'],
            phy_power=god['PhysicalPower'],
            phy_power_pl=god['PhysicalPowerPerLevel'],
            atk_speed=god['AttackSpeed'],
            atk_speed_pl=god['AttackSpeedPerLevel'],
            ability_passive=abilities[4],
            ability_1=abilities[0],
            ability_2=abilities[1],
            ability_3=abilities[2],
            ability_4=abilities[3]
        )

        if god['latestGod'] == 'y':
            god_new.latest_god = True

        print('Checking for {}...'.format(god['Name']))
        try:
            obj = God.objects.get(name=god['Name'])
            obj = god_new
            obj.save()
        except God.DoesNotExist:
            god_new.save()
            print('Adding {}...'.format(god['Name']))
