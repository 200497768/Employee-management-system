from .models import Office

class Offices:
    barrie_office:Office=Office(name='Barrie office',street='401 Duckworth Street',city='Barrie',province='Ontario',postal_code='postal',country='Canada',phone='705',group_name='Barrie')
    another_office:Office=Office(name='Another office',street='1 Another Street',city='Another',province='Ontario',postal_code='postal',country='Canada',phone='705',group_name='Another')
    offices:list[Office]=[barrie_office,another_office]

    def create(self)->None:
        for office in self.offices:
            office.save()