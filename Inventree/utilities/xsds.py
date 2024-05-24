

def get_user_xsd():
    return"""
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
        <xs:element name="user">
            <xs:complexType>
                <xs:sequence>
                    <xs:element name="routing_key">
                        <xs:simpleType>
                            <xs:restriction base="xs:string">
                                <xs:minLength value="1"/>
                            </xs:restriction>
                        </xs:simpleType>
                    </xs:element>
                    <xs:element name="crud_operation">
                        <xs:simpleType>
                            <xs:restriction base="xs:string">
                                <xs:enumeration value="create"/>
                                <xs:enumeration value="update"/>
                                <xs:enumeration value="delete"/>
                            </xs:restriction>
                        </xs:simpleType>
                    </xs:element>
                    <xs:element name="id">
                        <xs:simpleType>
                            <xs:restriction base="xs:string">
                                <xs:minLength value="1"/>
                            </xs:restriction>
                        </xs:simpleType>
                    </xs:element>
                    <xs:element name="first_name" type="xs:string" nillable="true"/>
                    <xs:element name="last_name" type="xs:string" nillable="true"/>
                    <xs:element name="email" type="xs:string" nillable="true"/>
                    <xs:element name="telephone" type="xs:string" nillable="true"/>
                    <xs:element name="birthday">
                        <xs:simpleType>
                            <xs:union>
                                <xs:simpleType>
                                    <xs:restriction base='xs:string'>
                                        <xs:length value="0"/>
                                    </xs:restriction>
                                </xs:simpleType>
                                <xs:simpleType>
                                    <xs:restriction base='xs:date' />
                                </xs:simpleType>
                            </xs:union>
                        </xs:simpleType>
                    </xs:element>
                    <xs:element name="address">
                        <xs:complexType>
                            <xs:sequence>
                                <xs:element name="country" type="xs:string" nillable="true"/>
                                <xs:element name="state" type="xs:string" nillable="true"/>
                                <xs:element name="city" type="xs:string" nillable="true"/>
                                <xs:element name="zip">
                                    <xs:simpleType>
                                        <xs:union>
                                            <xs:simpleType>
                                                <xs:restriction base='xs:string'>
                                                    <xs:length value="0"/>
                                                </xs:restriction>
                                            </xs:simpleType>
                                            <xs:simpleType>
                                                <xs:restriction base='xs:integer' />
                                            </xs:simpleType>
                                        </xs:union>
                                    </xs:simpleType>
                                </xs:element>
                                <xs:element name="street" type="xs:string" nillable="true"/>
                                <xs:element name="house_number">
                                    <xs:simpleType>
                                        <xs:union>
                                            <xs:simpleType>
                                                <xs:restriction base='xs:string'>
                                                    <xs:length value="0"/>
                                                </xs:restriction>
                                            </xs:simpleType>
                                            <xs:simpleType>
                                                <xs:restriction base='xs:integer' />
                                            </xs:simpleType>
                                        </xs:union>
                                    </xs:simpleType>
                                </xs:element>
                            </xs:sequence>
                        </xs:complexType>
                    </xs:element>
                    <xs:element name="company_email" type="xs:string" nillable="true"/>
                    <xs:element name="company_id" type="xs:string" nillable="true"/>
                    <xs:element name="source" type="xs:string"  nillable="true"/>
                    <xs:element name="user_role">
                        <xs:simpleType>
                            <xs:restriction base="xs:string">
                                <xs:enumeration value="speaker"/>
                                <xs:enumeration value="individual"/>
                                <xs:enumeration value="employee"/>
                                <xs:enumeration value=""/>
                            </xs:restriction>
                        </xs:simpleType>
                    </xs:element>
                    <xs:element name="invoice" type="xs:string" nillable="true"/>
                    <xs:element name="calendar_link" type="xs:string" nillable="true"/>
                </xs:sequence>
            </xs:complexType>
        </xs:element>
    </xs:schema>
    """